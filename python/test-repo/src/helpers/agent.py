import uuid
from typing import Literal, Union

from google.auth.exceptions import GoogleAuthError  # type: ignore
from langchain.agents import AgentExecutor, format_scratchpad, output_parsers
from langchain_core import prompts
from langchain_google_vertexai import ChatVertexAI
from langsmith import traceable

from src.core.config import ProjectConfig
from src.core.exceptions import ThirdPartyError
from src.helpers.log import Log
from src.helpers.utils import Utils


class BaseAgent:
    MAX_TOKENS: int = 4096

    def __init__(self, model_name: str = ProjectConfig.LLM_MODEL) -> None:
        self.model_name: str = model_name
        self.tools: list = []
        self.log: Log  # late
        self._set_up()

    def _set_up(self) -> None:
        """
        Prepare model, prompt template, and all essentials LLM.

        Raises:
            ThirdPartyError: raise if fail to initiate ChatVertexAI.
        """
        try:
            self._llm = ChatVertexAI(model_name=self.model_name)
        except GoogleAuthError as exc:
            self.log.error(
                msg="Fail to connect to ChatVertexAI", parent_func="BaseAgent._set_up"
            )
            raise ThirdPartyError(message=f"Fail to access Vertex: {exc}")

        if self.tools:
            self.llm = self.llm.bind_tools(tools=self.tools)  # type: ignore

        self.prompt: dict = {  # type: ignore
            "input": lambda x: x["input"],
            "agent_scratchpad": (
                lambda x: format_scratchpad.format_to_tool_messages(
                    x["intermediate_steps"]
                )
            ),
        } | prompts.ChatPromptTemplate.from_messages(
            [
                ("system", "You are a researcher expert with 15 years of experience."),
                ("user", "{input}"),
                prompts.MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    @traceable
    async def query(
        self, input: str, output_format: Literal["list", "dict"] = "dict"
    ) -> Union[dict, list]:
        """
        Call the LLM agent to execute the query.

        Args:
            input (dict): input prompt to be consumed by the agent.
            ai_id (str): request id.
            output_format (str): options are "list" and "dict".

        Raises:
            ThirdPartyError: raises when agent fail to invoke for whatever reason.

        Returns:
            dict: token outputs from LLM agent.
        """
        # initiate agent executor
        agent_executor = AgentExecutor(
            agent=(
                self.prompt  # type: ignore
                | self._llm.with_config(
                    {"run_id": uuid.UUID(self.log.log_detail["ai_id"])}
                )
                | output_parsers.ToolsAgentOutputParser()
            ),
            tools=[tool for tool in self.tools],
        )

        retry_count = 0
        while retry_count < 3:
            try:
                result = await agent_executor.ainvoke(
                    input={"input": input}, return_only_outputs=True
                )
            except Exception as exc:
                self.log.error(
                    msg=f"fail on agent invoke (retry {retry_count}): {exc}",
                    parent_func="BaseAgent.query",
                )
                retry_count += 1
                continue

            self.log.debug(
                msg=f"raw agent response: {result}", parent_func="BaseAgent.query"
            )

            try:
                # fail in cleaning ai result could be the result of inconsistent output format, retry!
                cleaned_result = Utils.clean_ai_result(
                    output=result["output"], format=output_format
                )
            except Exception as exc:
                self.log.error(
                    msg=f"fail on cleansing agent response (retry {retry_count}): {exc}",
                    parent_func="BaseAgent.query",
                )
                retry_count += 1
                continue

            return cleaned_result

        raise ThirdPartyError(
            message="Agent failure", ai_id=self.log.log_detail["ai_id"]
        )
