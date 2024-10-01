class ThirdPartyError(Exception):
    def __init__(self, message: str, ai_id: str = "") -> None:
        self.message = message
        self.ai_id = ai_id
        super().__init__(message)


class InternalError(Exception):
    def __init__(self, message: str, ai_id: str = "") -> None:
        self.message = message
        self.ai_id = ai_id
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str, ai_id: str) -> None:
        self.message = message
        self.ai_id = ai_id
        super().__init__(message)
