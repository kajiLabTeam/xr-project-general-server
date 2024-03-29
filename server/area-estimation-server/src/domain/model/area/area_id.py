from ulid import ULID


class AreaAggregateId:
    def __init__(self, id: ULID = ULID()):
        self.__id = id

    def get_id_of_private_value(self) -> ULID:
        return self.__id
