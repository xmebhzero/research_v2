import json
import logging
from queue import Queue

from fastapi import Request
from logging_loki import LokiQueueHandler  # type: ignore
from starlette.datastructures import QueryParams

from src.core.config import ProjectConfig
from src.helpers.const import LogSeverity, StatusMessage
from src.helpers.utils import Utils


class Log:
    def __init__(self) -> None:
        self._log_detail: dict = {}
        self._setup()

    def _setup(self) -> None:
        """
        Set log handler, formatter, etc.
        """
        self._loki_handler = LokiQueueHandler(
            queue=Queue(ProjectConfig.LOG_QUEUE_UNLIMITED),
            url=ProjectConfig.LOKI_URL,
            tags={
                "app": ProjectConfig.PROJECT_TITLE,
                "env": ProjectConfig.ENV,
            },
            version="1",
            auth=(
                ProjectConfig.LOKI_BASIC_AUTH_USERNAME,
                ProjectConfig.LOKI_BASIC_AUTH_PASSWORD,
            ),
        )

        self._logger = logging.getLogger("logger")
        self._logger.setLevel(logging.DEBUG)
        # ensure the LokiQueueHandler is added only once
        if not any(
            isinstance(handler, LokiQueueHandler) for handler in self._logger.handlers
        ):
            self._logger.addHandler(self._loki_handler)

    @property
    def log_detail(self) -> dict:
        """
        Log detail will have several components depends on the stage.

        Returns:
            dict: log_detail object
        """
        return self._log_detail

    @log_detail.setter
    def log_detail(self, value: dict) -> None:
        """
        Add or update dictionary key-value.

        Args:
            value (dict): given key-value that will be updated on to the log detail
        """
        if not isinstance(value, dict):
            raise ValueError("Expected a key-value")

        if self._log_detail:
            self._log_detail.update(value)

    async def store_log_pre_route(self, request: Request) -> None:
        """
        Log client request details.

        Args:
            request (Request): request object.
        """
        try:
            payload = await request.json()
        except Exception:
            payload = {}

        self._log_detail = {
            "request_id": request.headers.get("request-id", ""),
            "ai_id": Utils.generate_uuid4(),
            "msg": payload,
            "query_param": self._serialize_query_params(request.query_params),
            "path_param": request.path_params,
            "endpoint": request.url.path,
            "method": request.method,
            "version": ProjectConfig.VERSION,
            "type": "request",
            "severity": LogSeverity.INFO.value,
        }
        self.info(msg=self._log_detail)

    def _map_path_params_to_named_params(self, endpoint, path_params):
        """
        To map back value in path params to it's named params.

        Args:
        - endpoint (str): URL endpoint which contains path parameters.
        - path_params (dict): Dictionary of path parameters.

        Returns:
        - str: URL endpoint with named parameters.
        """
        for param, value in path_params.items():
            endpoint = endpoint.replace(f"/{value}", f"/{param}")
        return endpoint

    def store_log_post_route(
        self, *, request: Request, response: dict, status_code: int, time: float
    ) -> None:
        """
        Store request-response details..

        Args:
            request (Request): request object.
            response (dict): response details in dictionary format.
            status_code (int):
            time (float): time needed to execute the whole process.
        """
        if 200 <= status_code < 300:
            status = StatusMessage.SUCCESS.value
            severity = LogSeverity.INFO.value
        elif status_code >= 400:
            status = StatusMessage.FAIL.value
            severity = LogSeverity.ERROR.value
        else:
            status = ""
            severity = LogSeverity.DEFAULT.value

        if self._log_detail:
            self._log_detail["endpoint"] = self._map_path_params_to_named_params(
                self._log_detail["endpoint"], request.path_params
            )
            self._log_detail["code"] = status_code
            self._log_detail["msg"] = response
            self._log_detail["latency"] = time
            self._log_detail["status"] = status
            self._log_detail["severity"] = severity
            self._log_detail["type"] = "response"
            self.info(msg=self._log_detail)

    def _serialize_query_params(self, query_params: QueryParams) -> str:
        return "&".join([f"{key}={value}" for key, value in query_params.items()])

    def info(self, *, msg: dict) -> None:
        """
        Store log detail to the Loki with level INFO.
        This method is used only when accepting request and returning response.

        Args:
            msg_dict (dict): detail of the message.
        """
        self._logger.info(json.dumps(msg))

    def debug(self, *, msg: str, parent_func: str) -> None:
        """
        Store log detail to the Loki with level DEBUG.
        This method is used to trace the application.

        Args:
            msg (str): raw text.
            parent_func (str): on what function this method is called.
        """

        self._logger.debug(
            json.dumps(
                {
                    "request_id": self._log_detail.get("request_id", ""),
                    "ai_id": self._log_detail.get("ai_id", ""),
                    "parent_func": parent_func,
                    "message": msg,
                }
            )
        )

    def error(self, *, msg: str, parent_func: str) -> None:
        """
        Store log detail to the Loki with level ERROR.
        This method is called upon exception.

        Args:
            msg (str): raw text.
            parent_func (str): on what function this method is called.
        """
        self._logger.error(
            json.dumps(
                {
                    "request_id": self._log_detail.get("request_id", ""),
                    "ai_id": self._log_detail.get("ai_id", ""),
                    "parent_func": parent_func,
                    "message": msg,
                }
            )
        )
