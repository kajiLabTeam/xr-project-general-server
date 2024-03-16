from abc import ABCMeta, abstractmethod
from typing import List

from psycopg2.extensions import connection

from domain.model.spot.coordinate import Coordinate
from domain.model.spot_collection.aggregate import SpotCollectionAggregate


class SpotCollectionRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def find_for_coordinates(
        self,
        conn: connection,
        coordinates: List[Coordinate],
    ) -> SpotCollectionAggregate:
        pass
