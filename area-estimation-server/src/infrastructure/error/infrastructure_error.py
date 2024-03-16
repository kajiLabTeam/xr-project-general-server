class InfrastructureErrorType:
    COORDINATE_IS_NOT_FOUND = "coordinate is not found"
    SPOT_IS_NOT_FOUND = "spot is not found"


class InfrastructureError(Exception):
    def __init__(self, error_type: str, message: str):
        self._type = error_type
        self._message = message

    @property
    def type(self):
        return self._type

    @property
    def message(self):
        return self._message
