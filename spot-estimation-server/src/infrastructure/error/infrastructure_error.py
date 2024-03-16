class InfrastructureErrorType:
    COORDINATE_IS_NOT_FOUND = "coordinate is not found"
    SPOT_IS_NOT_FOUND = "spot is not found"
    FP_MODEL_IS_NOT_FOUND = "fp model is not found"
    RAW_DATA_IS_NOT_FOUND = "raw data is not found"
    TRANSMITTER_IS_NOT_FOUND = "transmitter is not found"
    COORDINATE_INSERT_ERROR = "coordinate insert error"
    SPOT_INSERT_ERROR = "spot insert error"
    FP_MODEL_INSERT_ERROR = "fp model insert error"
    RAW_DATA_INSERT_ERROR = "raw data insert error"
    TRANSMITTER_INSERT_ERROR = "transmitter insert error"


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
