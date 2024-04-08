from typing import Optional

from domain.models.fp_model.fp_model_id import FpModelAggregateId
from domain.models.spot.coordinate import Coordinate
from domain.models.spot.location_type import LocationType
from domain.models.spot.spot_id import SpotAggregateId
from domain.models.transmitter.aggregate import TransmitterAggregate
from ulid import ULID


class SpotAggregate:
    def __init__(
        self,
        name: str,
        floor: int,
        location_type: LocationType,
        coordinate: Coordinate,
        id: Optional[SpotAggregateId] = None,
    ) -> None:
        self.__id = id if id is not None else SpotAggregateId()
        self.__name = name
        self.__floor = floor
        self.__locationType = location_type
        self.__coordinate = coordinate
        self.__transmitter: TransmitterAggregate | None = None
        self.__fp_id: FpModelAggregateId | None = None

    def get_id_of_private_value(self) -> SpotAggregateId:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_floor_of_private_value(self) -> int:
        return self.__floor

    def get_location_type_of_private_value(self) -> LocationType:
        return self.__locationType

    def get_coordinate_of_private_value(self) -> Coordinate:
        return self.__coordinate

    def get_fp_id_of_private_value(self) -> FpModelAggregateId:
        if self.__fp_id is None:
            raise ValueError("fp_id is not set")
        return self.__fp_id

    def get_transmitter_id_of_private_value(self) -> TransmitterAggregate:
        if self.__transmitter is None:
            raise ValueError("transmitter_id is not set")
        return self.__transmitter

    def link_to_aggregate_fp_model(self, fp_model_id: FpModelAggregateId):
        self.fp_model_id = fp_model_id

    def link_to_aggregate_transmitter(self, transmitter: TransmitterAggregate):
        self.transmitter = transmitter


# ファクトリ:特定の引数を受け取ってドメインオブジェクトを生成するメソッド
class SpotAggregateFactory:
    @staticmethod
    def create(
        name: str,
        floor: int,
        location_type: str,
        latitude: float,
        longitude: float,
        id: str | None = None,
    ) -> SpotAggregate:
        if isinstance(id, str):
            __id = SpotAggregateId(ULID.from_str(id))
        else:
            __id = SpotAggregateId()
        __coordinate = Coordinate(latitude, longitude)
        __location_type = LocationType(location_type)
        return SpotAggregate(
            id=__id,
            name=name,
            floor=floor,
            location_type=__location_type,
            coordinate=__coordinate,
        )
