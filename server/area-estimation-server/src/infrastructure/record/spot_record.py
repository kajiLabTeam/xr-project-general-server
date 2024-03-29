from typing import List


class SpotRecord:
    def __init__(
        self,
        id: str,
        name: str,
        floors: int,
        location_type: str,
        created_at: str,
    ) -> None:
        self.__id = id
        self.__name = name
        self.__floors = floors
        self.__locationType = location_type
        self.__created_at = created_at

    def get_id_of_private_value(self) -> str:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_floors_of_private_value(self) -> int:
        return self.__floors

    def get_location_type_of_private_value(self) -> str:
        return self.__locationType

    def get_created_at_of_private_value(self) -> str:
        return self.__created_at


class SpotCollectionRecord:
    def __init__(self, spot_record_collection: List[SpotRecord]) -> None:
        self.__spot_record_collection = spot_record_collection

    def get_spot_record_collection_of_private_value(self) -> List[SpotRecord]:
        return self.__spot_record_collection
