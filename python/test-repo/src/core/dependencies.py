from src.core.config import ProjectConfig
from src.helpers.agent import BaseAgent
from src.helpers.aws import AWS
from src.helpers.db import Postgre

aws_client = AWS()

postgre_db = Postgre(
    user=ProjectConfig.DB_USERNAME,
    password=ProjectConfig.DB_PASSWORD,
    host=ProjectConfig.DB_HOST,
    port=ProjectConfig.DB_PORT,
    db_name=ProjectConfig.DB_NAME,
)

agent = None


def initialize_dependencies():
    global agent
    agent = BaseAgent()


def get_agent():
    global agent
    return agent
