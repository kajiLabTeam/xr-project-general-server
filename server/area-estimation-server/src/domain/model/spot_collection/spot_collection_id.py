from typing import Optional

from ulid import ULID


class SpotCollectionId:
    def __init__(self, id: Optional[ULID] = None) -> None:
        self.__id = id if id is not None else ULID()

    def get_id_of_private_value(self):
        return self.__id
