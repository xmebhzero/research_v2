import os

from dotenv import load_dotenv

load_dotenv()


class ProjectConfig:
    PROJECT_TITLE = "PopBot Service"
    DESCRIPTION = ""
    SUMMARY = "PopBot Service By Populix"
    VERSION = "1.0.0"
    TAGS_METADATA = None
    CONTACT = {"name": "SAT AI", "email": "ai@populix.co"}
    COMPANY_TIMEDELTA = 7  # UTC+7
    ENV = os.getenv("ENVIRONMENT", "")
    APP_HOST = "0.0.0.0"
    APP_PORT = 8000

    # LOG
    LOG_QUEUE_UNLIMITED = -1

    # DB
    DB_USERNAME = os.getenv("MVP_AI_USERNAME", "")
    DB_PASSWORD = os.getenv("MVP_AI_PASSWORD", "")
    DB_HOST = os.getenv("MVP_AI_HOST", "")
    DB_PORT = os.getenv("MVP_AI_PORT", "")
    DB_NAME = os.getenv("MVP_AI_DATABASE", "")

    # GCP
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
    GCP_LOG_NAME = os.getenv("GCP_LOG_NAME", "")
    GCP_LOG_BUCKET = os.getenv("GCP_LOG_BUCKET", "")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SA_KEY_PATH", "")

    # AWS
    AWS_S3_REGION = os.getenv("S3_REGION", "")
    AWS_S3_BUCKET = os.getenv("S3_REPORTING_BUCKET", "")
    os.environ["AWS_DEFAULT_REGION"] = AWS_S3_REGION
    os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # LLM
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "")
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "")
    LLM_MODEL = os.getenv("LANGCHAIN_MODEL", "")

    # External Party
    CLARIFY_HOST = os.getenv("CLARIFY_HOST", "")

    PROXY_HOST = os.getenv("PROXY_HOST", "")

    COVENA_HOST = os.getenv("COVENA_HOST", "")
    COVENA_CHATFLOW_ID_GPT4 = os.getenv("COVENA_CHATFLOW_ID_GPT4", "")
    COVENA_CHATFLOW_ID_SONNET = os.getenv("COVENA_CHATFLOW_ID_SONNET", "")

    LOKI_URL = os.getenv("LOKI_URL", "")
    LOKI_BASIC_AUTH_USERNAME = os.getenv("LOKI_BASIC_AUTH_USERNAME", "")
    LOKI_BASIC_AUTH_PASSWORD = os.getenv("LOKI_BASIC_AUTH_PASSWORD", "")
