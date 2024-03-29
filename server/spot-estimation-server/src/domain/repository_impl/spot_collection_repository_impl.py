from abc import ABCMeta, abstractmethod
from typing import List

from models.spot_collection.aggregate import SpotCollectionAggregate
from psycopg2.extensions import connection


class SpotCollectionRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def find_for_spot_id_collection(
        self,
        conn: connection,
        spot_id_collection: List[str],
    ) -> SpotCollectionAggregate:
        pass
