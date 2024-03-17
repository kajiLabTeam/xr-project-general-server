from abc import ABCMeta, abstractmethod

from domain.models.spot.aggregate import SpotAggregate
from domain.models.spot.spot_id import SpotAggregateId
from psycopg2.extensions import connection


class SpotRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def find_for_spot_id(
        self,
        conn: connection,
        spot_id: SpotAggregateId,
    ) -> SpotAggregate:
        pass

    @abstractmethod
    def save(
        self,
        conn: connection,
        spot: SpotAggregate,
    ) -> SpotAggregate:
        pass
