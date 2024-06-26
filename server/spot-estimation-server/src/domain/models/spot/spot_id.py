from typing import Optional

from ulid import ULID
from utils.ulid import generate_ulid


class SpotAggregateId:
    def __init__(self, id: Optional[ULID] = None):
        self.__id = id or generate_ulid()

    def get_id_of_private_value(self) -> str:
        return str(self.__id)
