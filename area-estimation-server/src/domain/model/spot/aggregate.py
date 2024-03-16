from ulid import ULID

from domain.model.spot.coordinate import Coordinate
from domain.model.spot.location_type import LocationType
from domain.model.spot.spot_id import SpotAggregateId


class SpotAggregate:
    def __init__(
        self,
        name: str,
        floors: int,
        location_type: LocationType,
        coordinate: Coordinate,
        id: SpotAggregateId = SpotAggregateId(),
    ) -> None:
        self.__id = id
        self.__name = name
        self.__floors = floors
        self.__locationType = location_type
        self.__coordinate = coordinate

    def get_id_of_private_value(self) -> SpotAggregateId:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_floors_of_private_value(self) -> int:
        return self.__floors

    def get_location_type_of_private_value(self) -> LocationType:
        return self.__locationType

    def get_coordinate_of_private_value(self) -> Coordinate:
        return self.__coordinate


# ファクトリ:特定の引数を受け取ってドメインオブジェクトを生成するメソッド
class SpotAggregateFactory:
    @staticmethod
    def create(
        name: str,
        floors: int,
        location_type: str,
        latitude: float,
        longitude: float,
        id: str = "",
    ) -> SpotAggregate:
        __spot_id = SpotAggregateId(ULID.from_str(id))
        __coordinate = Coordinate(latitude, longitude)
        __location_type = LocationType(location_type)
        if id == "":
            __spot_id = SpotAggregateId()

        return SpotAggregate(
            id=__spot_id,
            name=name,
            floors=floors,
            location_type=__location_type,
            coordinate=__coordinate,
        )
