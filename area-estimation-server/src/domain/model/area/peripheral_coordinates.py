from math import atan2, cos, radians, sin, sqrt
from typing import List

from config.const import EARTH_RADIUS, GENERATED_COORDINATES_NUM, PI
from domain.model.spot.coordinate import Coordinate


class PeripheralCoordinates:
    def __init__(
        self,
        radius: int,
        center_coordinate: Coordinate,
    ):
        self.peripheral_coordinate: List[Coordinate] = []
        self.add_peripheral_coordinate(center_coordinate)
        self.generate_coordinates_within_radius(center_coordinate, radius)

    def get_peripheral_coordinate_of_private_value(self) -> List[Coordinate]:
        return self.peripheral_coordinate

    def add_peripheral_coordinate(self, peripheral_coordinate: Coordinate):
        self.peripheral_coordinate.append(peripheral_coordinate)

    def remove_peripheral_coordinate(self, peripheral_coordinate: Coordinate):
        self.peripheral_coordinate.remove(peripheral_coordinate)

    # 中心座標と半径を受け取り、その中心座標を中心に半径内にある座標を生成する
    def generate_coordinates_within_radius(
        self, center_coordinate: Coordinate, radius: int
    ):
        # 角度を生成して、中心を中心にポイントを均等に分布させるポイント数を増やして、より均等に分布させる
        for i in range(GENERATED_COORDINATES_NUM):
            angle = 2 * PI * (i / GENERATED_COORDINATES_NUM)
            dx = radius * cos(angle)
            dy = radius * sin(angle)

            # 新しい緯度と経度を計算する
            new_latitude = center_coordinate.get_latitude_of_private_value() + (
                dy / EARTH_RADIUS
            ) * (180 / PI)
            new_longitude = center_coordinate.get_longitude_of_private_value() + (
                dx
                / (
                    EARTH_RADIUS
                    * cos(radians(center_coordinate.get_latitude_of_private_value()))
                )
            ) * (180 / PI)

            self.add_peripheral_coordinate(Coordinate(new_latitude, new_longitude))

    # 2つの座標間の距離を計算する
    # NOTE : このメソッドは現在使用されていませんが、将来的に使用する可能性があります
    def calculate_distance(self, coord1: Coordinate, coord2: Coordinate) -> float:
        # 2つの座標間の距離を計算するHaversineの公式
        lat1, lon1 = radians(coord1.get_latitude_of_private_value()), radians(
            coord1.get_longitude_of_private_value()
        )
        lat2, lon2 = radians(coord2.get_latitude_of_private_value()), radians(
            coord2.get_longitude_of_private_value()
        )

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = EARTH_RADIUS * c
        return distance
