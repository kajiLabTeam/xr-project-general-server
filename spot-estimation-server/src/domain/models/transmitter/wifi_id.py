from ulid import ULID
from utils.ulid import generate_ulid


class WifiId:
    def __init__(self):
        self.__id: ULID = generate_ulid()

    def get_id_of_private_value(self) -> str:
        return str(self.__id)
