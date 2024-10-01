import ast
import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Union

import httpx


class Utils:
    @staticmethod
    def get_current_timestamp(delta: int) -> datetime:
        """
        Get current timestamp on the specific timezone.

        Args:
            delta (int): hours difference from UTC

        Returns:
            datetime: current timestamp on specific timezone
        """
        utc_zone = timezone(offset=timedelta(hours=delta))
        return datetime.now(utc_zone)

    @staticmethod
    def generate_uuid4() -> str:
        """
        Generate UUID, mainly to trace application log.

        Returns:
            str: uuid 4 in string representation
        """
        return str(uuid.uuid4())

    @staticmethod
    async def call_url_async(
        url: str, method: str, body: dict | None = None
    ) -> httpx.Response:
        """
        Call url asynchronously.

        Args:
            url (str): url target.
            method (str): HTTP method.
            body (dict | None, optional): body JSON if method is POST. Defaults to None.
        """
        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(url=url, json=body, timeout=None)
            elif method == "PUT":
                response = await client.put(url=url, json=body, timeout=None)
            else:
                raise NotImplementedError()

        return response

    @staticmethod
    def sanitize_string(input_string: str) -> str:
        """
        Sanitize string by removing single quote and backtick.

        Args:
            input_string (str): input string

        Returns:
            str: sanitized string
        """
        return input_string.replace("'", "").replace("`", "")

    @staticmethod
    def sanitize_value(value: Any) -> Any:
        """
        Sanitize value by removing single quote and backtick.

        Args:
            value: value to be sanitized

        Returns:
            value: sanitized value
        """
        if isinstance(value, str):
            return Utils.sanitize_string(value)
        elif isinstance(value, list):
            return [Utils.sanitize_value(item) for item in value]
        elif isinstance(value, dict):
            return {
                Utils.sanitize_string(k): Utils.sanitize_value(v)
                for k, v in value.items()
            }
        return value

    @staticmethod
    def remove_quote_and_backtick(input: dict) -> dict:
        """
        Remove single quote and backtick from dictionary.

        Args:
            input (dict): input dictionary

        Returns:
            dict: sanitized dictionary
        """
        return {
            Utils.sanitize_string(k): Utils.sanitize_value(v) for k, v in input.items()
        }

    @staticmethod
    def sanitize_ai_input(input: dict) -> dict:
        """
        Sanitize AI input by removing single quote and backtick.

        Args:
            input (dict): AI input

        Returns:
            dict: sanitized AI input
        """
        result = Utils.remove_quote_and_backtick(input)
        # add more sanitization here if needed

        return result

    @staticmethod
    def clean_ai_result(
        output: str, format: Literal["list", "dict"]
    ) -> Union[dict, list]:
        """
        Cleaned AI result.

        Args:
            output (str): AI output

        Returns:
            dict, list: cleaned AI output
        """
        if format not in ["list", "dict"]:
            raise NotImplementedError(
                "Only able to clean LLM output to 'list' or 'dict'"
            )

        if format == "dict":
            return Utils._convert_json_string_to_dict(json_str=output)
        else:  # list
            return Utils._convert_json_string_to_list(json_str=output)

    @staticmethod
    def _convert_json_string_to_dict(json_str: str) -> dict:
        """
        Convert json string to dictionary.

        Args:
            input (str): json in string representation.

        Returns:
            dict: converted input in dict format.
        """
        if "```" in json_str:
            splitted_json_str = json_str.split("```")
            json_str = splitted_json_str[1]
        else:
            json_str = json_str

        # handle json code block from LLM
        json_str = (
            json_str.replace("JSON", "")
            .replace("json", "")
            .replace("js", "")
            .replace("python", "")
        )

        try:
            output_json = json.loads(json_str)
        except json.JSONDecodeError:
            # handle single and double quote issue
            json_str = re.sub(r"(?<!\\)'", '"', json_str)
            output_json = json.loads(json_str)

        return output_json

    @staticmethod
    def _convert_json_string_to_list(json_str: str) -> list:
        """
        Convert json string to list.

        Args:
            input (str): json in string representation.

        Returns:
            list: converted input in list format.
        """
        splitted_json_str = json_str.split(" = ")
        json_str = splitted_json_str[1]

        return ast.literal_eval(json_str)

    @staticmethod
    def convert_list_to_numbered_string(input: list[str]) -> str:
        """
        Convert list to string with numbering.

        Args:
            input (list[str]): list of string._

        Returns:
            str: converted format.
        """
        converted: str = ""
        for index, element in enumerate(input, start=1):
            converted += f"({index}). {element} \n"

        return converted

    @staticmethod
    def convert_snake_to_camel_case(input: str) -> str:
        """
        Convert snake case to camel case. First letter always in lowercase meanwhile
        the next word will have the first letter in uppercase.

        Args:
            input (str): input string.

        Returns:
            str: input string converted to camel case.
        """
        input_list = input.split("_")
        input_camel_case = input_list[0] + "".join(
            word.title() for word in input_list[1:]
        )

        return input_camel_case

    @staticmethod
    def convert_dict_keys_to_camel_case(input: dict) -> dict:
        """
        Convert original input with key data formatted in snake case to camel case.

        Args:
            input (dict): input dictionary.

        Returns:
            dict: dictionary with key converted to camel case style.
        """
        converted_input: dict = {}
        for key, value in input.items():
            key = Utils.convert_snake_to_camel_case(input=key)
            if isinstance(value, dict):
                converted_input[key] = Utils.convert_dict_keys_to_camel_case(
                    input=value
                )
            elif isinstance(value, list):
                converted_nested_input = []
                for val in value:
                    val = Utils.convert_dict_keys_to_camel_case(input=val)
                    converted_nested_input.append(val)
                converted_input[key] = converted_nested_input
            else:
                converted_input[key] = value

        return converted_input

    @staticmethod
    def convert_keys_to_snake_case(input: Union[dict, list]) -> Union[dict, list]:
        """
        Convert original input with data formatted in camel case to snake case.

        Args:
            input (Union[dict, list]): input data.

        Returns:
            list, dict: input with key formatted to snake case.
        """
        if isinstance(input, list):
            return [Utils.convert_keys_to_snake_case(item) for item in input]
        elif isinstance(input, dict):
            new_dict = {}
            for key, value in input.items():
                new_key = "".join(
                    ["_" + c.lower() if c.isupper() else c for c in key]
                ).lstrip("_")
                new_dict[new_key] = Utils.convert_keys_to_snake_case(value)
            return new_dict
        else:
            return input
