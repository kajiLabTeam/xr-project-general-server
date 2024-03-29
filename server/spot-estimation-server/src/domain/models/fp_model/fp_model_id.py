from ulid import ULID
from utils.ulid import generate_ulid


class FpModelAggregateId:
    def __init__(self):
        self.__id = generate_ulid()

    def get_id_of_private_value(self) -> str:
        return str(self.__id)

    def generate_ulid(self) -> ULID:
        return ULID()
