from domain.model.area.aggregate import AreaAggregate
from domain.model.spot_collection.aggregate import SpotCollectionAggregate
from domain.repository_impl.spot_collection_repository_impl import \
    SpotCollectionRepositoryImpl
from infrastructure.connection import DBConnection


class GetSpotCollectionByAreaService:
    def __init__(
        self,
        spot_collection_repository: SpotCollectionRepositoryImpl,
    ):
        self.__spot_collection_repository = spot_collection_repository

    def run(self, area: AreaAggregate) -> SpotCollectionAggregate:
        conn = DBConnection.connect()

        # エリアを元にリポジトリからスポットを取得
        spot_collection = self.__spot_collection_repository.find_for_coordinates(
            conn=conn,
            coordinates=area.get_peripheral_coordinate_of_private_value().get_peripheral_coordinate_of_private_value(),
        )

        return spot_collection
