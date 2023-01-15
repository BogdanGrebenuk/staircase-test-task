class RecognitionBaseException(Exception):

    def __init__(self, message, payload=None):
        if payload is None:
            payload = {}
        super().__init__(message)
        self.payload = payload


class CallbackUrlIsNotValid(RecognitionBaseException):
    ... # todo
