import json
import os
import time

from fastapi import BackgroundTasks, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.helpers.log import Log


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Main entry point when any endpoint is called by the client.

        Args:
            request (Request): _description_
            call_next (RequestResponseEndpoint): _description_

        Returns:
            Response: _description_
        """
        start_time = time.time()

        request.state.log = Log()
        await request.state.log.store_log_pre_route(request=request)

        response = await call_next(request)
        total_time: float = round(time.time() - start_time, 5)

        response, response_body = await self._parse_response(response=response)
        request.state.log.store_log_post_route(
            request=request,
            response=response_body,
            status_code=response.status_code,
            time=total_time,
        )

        is_testing: bool = os.environ.get("TESTING") == "true"

        if not is_testing:
            if not hasattr(response, "background") or (
                hasattr(response, "background") and response.background is None
            ):
                # response.background = BackgroundTasks()
                pass
            elif hasattr(response, "background") and isinstance(
                response.background, BackgroundTasks
            ):
                pass

        return response

    async def _parse_response(self, response: Response) -> tuple:
        """
        Parse Response object to get the body.
        Bare Response class is a stream response, thus we need additional process
        to parse the body.

        Args:
            response (Response): response object from view function.

        Returns:
            tuple: res
        """
        resp_body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

        try:
            resp_body = json.loads(resp_body[0].decode())
        except Exception:
            resp_body = str(resp_body)

        return response, resp_body


class AsyncIteratorWrapper:
    """
    Utility class to transforms a regular iterable to asynchronous one.

    Reference: https://medium.com/@dhavalsavalia/fastapi-logging-middleware-logging-requests-and-responses-with-ease-and-style-201b9aa4001a
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
