from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Cores
from src.core.config import ProjectConfig
from src.core.dependencies import initialize_dependencies
from src.core.exceptions import InternalError, NotFoundError, ThirdPartyError
from src.core.middleware import CustomMiddleware

# Helpers
from src.helpers.const import StatusMessage
from src.helpers.response import BaseFailResponse

# ROUTES
from src.modules.information import info_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    initialize_dependencies()
    yield


app = FastAPI(
    title=ProjectConfig.PROJECT_TITLE,
    description=ProjectConfig.DESCRIPTION,
    summary=ProjectConfig.SUMMARY,
    openapi_tags=ProjectConfig.TAGS_METADATA,
    version=ProjectConfig.VERSION,
    contact=ProjectConfig.CONTACT,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)

app.add_middleware(CustomMiddleware)

app.include_router(info_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    This exception overwrites typical 422 due to pydantic validation logic.
    """
    return JSONResponse(
        content=BaseFailResponse(
            status=StatusMessage.FAIL.value,
            message="Validation error. Please check your path param, query param or body request.",
            ai_id=request.state.log.log_detail["ai_id"],
        ).model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(InternalError)
def internal_error_handler(request: Request, exc: InternalError) -> JSONResponse:
    return JSONResponse(
        content=BaseFailResponse(
            status=StatusMessage.FAIL.value,
            message=exc.message,
            ai_id=request.state.log.log_detail["ai_id"],
        ).model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(ThirdPartyError)
def third_party_error_handler(request: Request, exc: ThirdPartyError) -> JSONResponse:
    return JSONResponse(
        content=BaseFailResponse(
            status=StatusMessage.FAIL.value,
            message=exc.message,
            ai_id=request.state.log.log_detail["ai_id"],
        ).model_dump(),
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@app.exception_handler(NotFoundError)
def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        content=BaseFailResponse(
            status=StatusMessage.FAIL.value,
            message=exc.message,
            ai_id=request.state.log.log_detail["ai_id"],
        ).model_dump(),
        status_code=status.HTTP_404_NOT_FOUND,
    )


if __name__ == "__main__":
    import os

    import uvicorn

    cpu = os.cpu_count()
    if cpu is None:  # due to unsuppoted OS, restricted environments, etc
        cpu = 1  # base spec
    workers = cpu * 2

    uvicorn.run(
        "main:app",
        host=ProjectConfig.APP_HOST,
        port=ProjectConfig.APP_PORT,
        workers=workers,
        access_log=True,
        reload=False,
    )