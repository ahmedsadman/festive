class BaseError(Exception):
    '''Base Error class'''

    def __init__(self, status=400, message=None, payload=None, error=None):
        super().__init__(self)
        self.status = status
        self.message = message
        self.payload = payload
        self.error = error

    def to_dict(self):
        d = dict()
        d['status'] = self.status
        d['message'] = self.message
        if self.error:
            d['error'] = self.error
        if self.payload and type(self.payload) == dict:
            d.update(self.payload)
        return d


class BadRequest(BaseError):
    def __init__(self, message='Bad request', payload=None):
        super().__init__(self, message, payload)
        self.status = 400


class NotFound(BaseError):
    def __init__(self, message='Not Found', payload=None):
        super().__init__(self, message, payload)
        self.status = 404


class ServerError(BaseError):
    def __init__(self, message='Internal server error', payload=None, error=None):
        super().__init__(self, message, payload, error)
        self.status = 500
