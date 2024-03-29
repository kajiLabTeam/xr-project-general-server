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
    def __init__(self, coordinate_list: List[CoordinateRecord]):
        self.__coordinate_list = coordinate_list

    def get_coordinate_list_of_private_value(self) -> List[CoordinateRecord]:
        return self.__coordinate_list

    def add_coordinate(self, coordinate: CoordinateRecord):
        self.__coordinate_list.append(coordinate)

    def unique_coordinate(self) -> None:
        """
        idをキーにして重複を削除する
        """
        unique_coordinates_dict = {
            coordinate.get_id_of_private_value(): coordinate
            for coordinate in self.__coordinate_list
        }
        self.__coordinate_list = list(unique_coordinates_dict.values())

    # CoordinateRecordのspot_idを抽出する
    def extract_spot_id(self) -> List[str]:
        return [
            coordinate.get_spot_id_of_private_value()
            for coordinate in self.__coordinate_list
        ]
