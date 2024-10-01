from enum import Enum


class StatusMessage(Enum):
    SUCCESS = "success"
    FAIL = "fail"


class LogSeverity(Enum):
    DEFAULT = "DEFAULT"
    ERROR = "ERROR"
    INFO = "INFO"
