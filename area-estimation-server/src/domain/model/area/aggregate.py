from domain.error.domain_error import DomainError, DomainErrorType
from domain.model.area.area_id import AreaAggregateId
from domain.model.area.peripheral_coordinates import PeripheralCoordinates
from domain.model.spot.coordinate import Coordinate


class AreaAggregate:
    def __init__(
        self,
        radius: int,
        center_coordinate: Coordinate,
    ) -> None:
        if radius < 0:
            raise DomainError(
                DomainErrorType.RADIUS_TAKE_A_NEGATIVE_VALUE,
                "radius take a negative value",
            )

        self.__id = AreaAggregateId()
        self.__radius = radius
        self.__center_coordinate = center_coordinate
        self.__peripheral_coordinate = PeripheralCoordinates(
            radius=radius,
            center_coordinate=center_coordinate,
        )

    def get_id_of_private_value(self) -> AreaAggregateId:
        return self.__id

    def get_radius_of_private_value(self) -> int:
        return self.__radius

    def get_coordinate_of_private_value(self) -> Coordinate:
        return self.__center_coordinate

    def get_peripheral_coordinate_of_private_value(self) -> PeripheralCoordinates:
        return self.__peripheral_coordinate


# ファクトリ:特定の引数を受け取ってドメインオブジェクトを生成するメソッド
class AreaAggregateFactory:
    @staticmethod
    def create(
        radius: int,
        latitude: float,
        longitude: float,
    ) -> AreaAggregate:
        __coordinate = Coordinate(latitude, longitude)
        return AreaAggregate(
            radius=radius,
            center_coordinate=__coordinate,
        )
