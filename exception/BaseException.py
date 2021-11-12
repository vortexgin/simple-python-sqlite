class BaseException(Exception):
    message = "Error!"
    status_code = 500

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        response = {
            'code': self.status_code,
            'message': self.message
        }
        if self.payload is not None:
            response['payload'] = self.payload
        
        return response