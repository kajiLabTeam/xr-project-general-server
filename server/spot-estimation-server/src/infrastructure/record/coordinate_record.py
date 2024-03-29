from typing import List


class CoordinateRecord:
    def __init__(
        self,
        id: str,
        latitude: float,
        longitude: float,
        spot_id: str,
    ):
        self.__id = id
        self.__latitude = latitude
        self.__longitude = longitude
        self.__spot_id = spot_id

    def get_id_of_private_value(self) -> str:
        return self.__id

    def get_latitude_of_private_value(self) -> float:
        return self.__latitude

    def get_longitude_of_private_value(self) -> float:
        return self.__longitude

    def get_spot_id_of_private_value(self) -> str:
        return self.__spot_id


class CoordinateCollectionRecord:
    def __init__(self, coordinates: List[CoordinateRecord]):
        self.__coordinates = coordinates

    def get_coordinates_of_private_value(self) -> List[CoordinateRecord]:
        return self.__coordinates

    # CoordinateRecordのspot_idを抽出する
    def extract_spot_id(self) -> List[str]:
        return [
            coordinate.get_spot_id_of_private_value()
            for coordinate in self.__coordinates
        ]
