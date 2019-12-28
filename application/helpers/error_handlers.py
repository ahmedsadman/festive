class BaseError(Exception):
    """Base Error class"""

    def __init__(self, message=None, error=None):
        super().__init__(self)
        self.message = message
        self.error = error

    def to_dict(self):
        d = dict()
        d["status"] = self.status
        d["message"] = self.message
        if self.error:
            d["error"] = self.error
        return d


class BadRequest(BaseError):
    def __init__(self, message="Bad request", error=None):
        super().__init__(message, error)
        self.status = 400


class FieldValidationFailed(BaseError):
    def __init__(self, message="Field validation failed", error=None):
        super().__init__(message, error)
        self.status = 400


class NotFound(BaseError):
    def __init__(self, message="Not Found"):
        super().__init__(message)
        self.status = 404


class AuthorizationError(BaseError):
    INVALID_CRED = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED = "TOKEN_EXPIRED"

    def __init__(self, message="Unauthorized", error=None):
        super().__init__(message, error)
        self.status = 401


class ServerError(BaseError):
    def __init__(self, message="Internal server error", error=None):
        super().__init__(message, error)
        self.status = 500
