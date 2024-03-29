from ulid import ULID


class SpotCollectionId:
    def __init__(self, id: ULID = ULID()):
        self.__id = id

    def get_id_of_private_value(self):
        return self.__id
