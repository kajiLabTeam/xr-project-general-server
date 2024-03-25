from math import asin, atan2, cos, degrees, radians, sin
from typing import List, Tuple

from config.const import (ANGLE_OF_CIRCLE, ANGLE_THRESHOLD, EARTH_RADIUS,
                          ROUNDING_PRECISION)
from domain.model.spot.coordinate import Coordinate


class CircumferentialCoordinates:
    def __init__(
        self,
        radius: int,
        center_coordinate: Coordinate,
    ):
        self.peripheral_coordinate: List[Coordinate] = []
        self.add_circumferential_coordinate(center_coordinate)
        self.generate_coordinates_within_radius(center_coordinate, radius)

    def get_peripheral_coordinate_of_private_value(self) -> List[Coordinate]:
        return self.peripheral_coordinate

    def add_circumferential_coordinate(self, circumferential_coordinate: Coordinate):
        self.peripheral_coordinate.append(circumferential_coordinate)

    def remove_peripheral_coordinate(self, circumferential_coordinate: Coordinate):
        self.peripheral_coordinate.remove(circumferential_coordinate)

    def __calculate_point(
        self, center_coordinate: Coordinate, radius: int, angle: float
    ) -> Tuple[float, float]:
        """
        中心点、半径、方位角から円周上の点を計算する
        """

        # 緯度と経度を度からラジアンに変換します
        lat1 = radians(center_coordinate.get_latitude_of_private_value())
        lon1 = radians(center_coordinate.get_longitude_of_private_value())
        angular_distance = radius / EARTH_RADIUS

        # 方位角を度からラジアンに変換します
        angle = radians(angle)

        lat2 = asin(
            sin(lat1) * cos(angular_distance)
            + cos(lat1) * sin(angular_distance) * cos(angle)
        )
        lon2 = lon1 + atan2(
            sin(angle) * sin(angular_distance) * cos(lat1),
            cos(angular_distance) - sin(lat1) * sin(lat2),
        )

        # ラジアンから度に緯度と経度を変換し、小数点第六位まで丸めます
        lat2 = round(degrees(lat2), ROUNDING_PRECISION)
        lon2 = round(degrees(lon2), ROUNDING_PRECISION)

        return lat2, lon2

    def generate_coordinates_within_radius(
        self, center_coordinate: Coordinate, radius: int
    ):
        """
        中心座標と半径を受け取り、その中心座標を中心に半径内にある座標を生成する
        """
        for bearing in range(0, ANGLE_OF_CIRCLE, ANGLE_THRESHOLD):
            lat, lon = self.__calculate_point(
                center_coordinate=center_coordinate, radius=radius, angle=bearing
            )
            self.add_circumferential_coordinate(Coordinate(latitude=lat, longitude=lon))
