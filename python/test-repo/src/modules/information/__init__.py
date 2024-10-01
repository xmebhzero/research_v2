from fastapi import APIRouter, status

from src.modules.information.schemas import HealthSuccessResponse, InfoSuccessResponse
from src.modules.information.views import api_info_view, health_check_view

info_router = APIRouter(tags=["Information"])
info_router.add_api_route(
    path="/",
    endpoint=api_info_view,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": InfoSuccessResponse,
            "description": "Success response structure.",
        }
    },
)
info_router.add_api_route(
    path="/health",
    endpoint=health_check_view,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": HealthSuccessResponse,
            "description": "Success response structure.",
        }
    },
)
