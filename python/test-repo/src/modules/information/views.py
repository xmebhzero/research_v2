from fastapi import status
from fastapi.responses import JSONResponse

from src.core.config import ProjectConfig
from src.helpers.const import StatusMessage
from src.helpers.utils import Utils
from src.modules.information.schemas import HealthSuccessResponse, InfoSuccessResponse


async def api_info_view() -> JSONResponse:
    """
    View function to get the application information.

    \f
    Returns:
        JSONResponse: application information.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=InfoSuccessResponse(
            status=StatusMessage.SUCCESS.value,
            service_name=ProjectConfig.PROJECT_TITLE,
            environment=ProjectConfig.ENV,
            version=ProjectConfig.VERSION,
        ).model_dump(),
    )


async def health_check_view() -> JSONResponse:
    """
    View function to check whether the application is up or not.

    \f
    Returns:
        JSONResponse: application health information.
    """
    current_timestamp = Utils.get_current_timestamp(
        delta=ProjectConfig.COMPANY_TIMEDELTA
    ).isoformat()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=HealthSuccessResponse(
            status="healthy",
            last_heartbeat=current_timestamp,
            version=ProjectConfig.VERSION,
        ).model_dump(),
    )
