class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(BaseError):
    pass


class ValidationError(BaseError):
    pass
