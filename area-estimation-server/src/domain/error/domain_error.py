class DomainErrorType:
    RADIUS_TAKE_A_NEGATIVE_VALUE = "radius take a negative value"
    INVALID_LATITUDE = "latitude is invalid"
    INVALID_LONGITUDE = "longitude is invalid"
    INVALID_LOCATION = "location is invalid"


class DomainError(Exception):
    def __init__(self, type: str, message: str):
        self._type = type
        self._message = message

    @property
    def type(self):
        return self._type

    @property
    def message(self):
        return self._message
