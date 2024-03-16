from abc import ABCMeta, abstractmethod

from psycopg2.extensions import connection

from domain.models.spot.aggregate import SpotAggregate
from domain.models.spot.spot_id import SpotAggregateId


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
