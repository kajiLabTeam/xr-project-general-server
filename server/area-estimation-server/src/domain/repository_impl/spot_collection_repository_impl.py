from abc import ABCMeta, abstractmethod
from typing import List

from domain.model.spot.coordinate import Coordinate
from domain.model.spot_collection.aggregate import SpotCollectionAggregate
from psycopg2.extensions import connection


class SpotCollectionRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def find_for_coordinate_list(
        self,
        conn: connection,
        center_coordinate: Coordinate,
        circumferential_coordinate_list: List[Coordinate],
    ) -> SpotCollectionAggregate:
        pass
