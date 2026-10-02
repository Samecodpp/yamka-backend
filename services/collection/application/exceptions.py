class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(BaseError):
    """Raised when a resource is not found."""

    pass


class ValidationError(BaseError):
    """Raised when input data fails domain validation."""

    pass
