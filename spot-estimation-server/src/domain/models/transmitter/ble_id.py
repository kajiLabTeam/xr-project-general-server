from utils.ulid import generate_ulid


class BleId:
    def __init__(self):
        self.__id = generate_ulid()

    def get_id_of_private_value(self) -> str:
        return str(self.__id)
