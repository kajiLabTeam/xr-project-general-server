from domain.model.area.aggregate import AreaAggregate
from domain.model.spot_collection.aggregate import SpotCollectionAggregate
from domain.repository_impl.spot_collection_repository_impl import \
    SpotCollectionRepositoryImpl
from infrastructure.connection import DBConnection
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)


class GetSpotCollectionByAreaService:
    def __init__(
        self,
        spot_collection_repository: SpotCollectionRepositoryImpl,
    ):
        self.__spot_collection_repository = spot_collection_repository

    def run(self, area: AreaAggregate) -> SpotCollectionAggregate | None:
        conn = DBConnection.connect()

        try:
            # エリアを元にリポジトリからスポットを取得
            spot_collection = self.__spot_collection_repository.find_for_coordinate_list(
                conn=conn,
                center_coordinate=area.get_coordinate_of_private_value(),
                circumferential_coordinate_list=area.get_peripheral_coordinate_of_private_value(),
            )

            return spot_collection
        except InfrastructureError as e:
            if (
                e.type is InfrastructureErrorType.COORDINATE_IS_NOT_FOUND
                or e.type is InfrastructureErrorType.SPOT_IS_NOT_FOUND
            ):
                return None
        finally:
            conn.close()
