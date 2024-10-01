from src.core.config import ProjectConfig
from src.helpers.const import StatusMessage
from src.helpers.response import BaseResponse


class InfoSuccessResponse(BaseResponse):
    service_name: str
    environment: str

    class Config:
        json_schema_extra = {
            "example": {
                "version": ProjectConfig.VERSION,
                "status": StatusMessage.SUCCESS.value,
                "environment_name": ProjectConfig.ENV,
                "service_name": ProjectConfig.PROJECT_TITLE,
            }
        }


class HealthSuccessResponse(BaseResponse):
    last_heartbeat: str

    class Config:
        json_schema_extra = {
            "example": {
                "version": ProjectConfig.VERSION,
                "status": StatusMessage.SUCCESS.value,
                "last_heartbeat": "2024-05-30T13:09:11.141394+07:00",
            }
        }
