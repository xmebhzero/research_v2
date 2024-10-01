from pydantic import BaseModel, StrictStr

from src.core.config import ProjectConfig
from src.helpers.const import StatusMessage


class BaseResponse(BaseModel):
    version: str = ProjectConfig.VERSION
    status: str = StatusMessage.SUCCESS.value


class AISuccessBaseResponse(BaseResponse):
    ai_id: StrictStr


class BaseFailResponse(BaseResponse):
    message: str
    status: str = StatusMessage.FAIL.value
    ai_id: StrictStr

    class Config:
        json_schema_extra = {
            "example": {
                "version": ProjectConfig.VERSION,
                "status": StatusMessage.FAIL.value,
                "message": "Validation error. Please check your path param, query param or body request.",
                "ai_id": "3068037d-ab1c-44ae-bd72-c26af29bf804",
            }
        }
