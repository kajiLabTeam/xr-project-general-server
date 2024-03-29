from typing import List

from domain.model.spot.aggregate import SpotAggregate
from domain.model.spot_collection.spot_collection_id import SpotCollectionId


class SpotCollectionAggregate:
    def __init__(
        self,
        spot_collection: List[SpotAggregate],
    ):
        self.__id = SpotCollectionId()
        self.__spot_collection: List[SpotAggregate] = spot_collection

    def get_id_of_private_value(self) -> SpotCollectionId:
        return self.__id

    def get_spot_collection_of_private_value(self) -> List[SpotAggregate]:
        return self.__spot_collection

    def add_spot(self, spot: SpotAggregate) -> None:
        self.__spot_collection.append(spot)

    def remove_spot(self, spot: SpotAggregate) -> None:
        self.__spot_collection.remove(spot)


class SpotCollectionAggregateFactory:
    @staticmethod
    def create(
        spot_collection: List[SpotAggregate],
    ) -> SpotCollectionAggregate:
        return SpotCollectionAggregate(
            spot_collection=spot_collection,
        )
