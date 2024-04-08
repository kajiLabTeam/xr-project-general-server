from typing import List

from domain.model.spot.aggregate import SpotAggregateFactory
from domain.model.spot.coordinate import Coordinate
from domain.model.spot_collection.aggregate import (
    SpotCollectionAggregate, SpotCollectionAggregateFactory)
from domain.repository_impl.spot_collection_repository_impl import \
    SpotCollectionRepositoryImpl
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)
from infrastructure.gateway.coordinate_gateway import CoordinateGateway
from infrastructure.gateway.spot_gateway import SpotGateway
from psycopg2.extensions import connection

spot_gateway = SpotGateway()
coordinate_gateway = CoordinateGateway()


class SpotCollectionRepository(SpotCollectionRepositoryImpl):
    def find_for_coordinate_list(
        self,
        conn: connection,
        center_coordinate: Coordinate,
        circumferential_coordinate_list: List[Coordinate],
    ) -> SpotCollectionAggregate:
        # ゲートウェイに引数として渡すためのリストを作成
        circumferential_latitude_list = [
            circumferential_coordinate.get_latitude_of_private_value()
            for circumferential_coordinate in circumferential_coordinate_list
        ]
        circumferential_longitude_list = [
            circumferential_coordinate.get_longitude_of_private_value()
            for circumferential_coordinate in circumferential_coordinate_list
        ]

        # 座標リストをデータベースからスポットIDリストを元に取得
        coordinate_collection_select_record = (
            coordinate_gateway.find_for_coordinate_list(
                conn,
                center_coordinate.get_latitude_of_private_value(),
                center_coordinate.get_longitude_of_private_value(),
                circumferential_latitude_list,
                circumferential_longitude_list,
            )
        )
        print(coordinate_collection_select_record)
        if coordinate_collection_select_record is None:
            raise InfrastructureError(
                InfrastructureErrorType.COORDINATE_IS_NOT_FOUND,
                "coordinate is not found",
            )

        print(coordinate_collection_select_record.extract_spot_id())

        # スポットIDリストを元にスポットリストを取得
        spot_collection_select_record = spot_gateway.find_by_spot_ids(
            conn,
            coordinate_collection_select_record.extract_spot_id(),
        )
        if spot_collection_select_record is None:
            raise InfrastructureError(
                InfrastructureErrorType.SPOT_IS_NOT_FOUND,
                "spot is not found",
            )

        # HACK: レコードのメソッドを使ってもう少し簡潔に書けるかもしれない
        spot_collection = SpotCollectionAggregateFactory.create(
            spot_collection=[
                SpotAggregateFactory.create(
                    id=spot_record.get_id_of_private_value(),
                    name=spot_record.get_name_of_private_value(),
                    floors=spot_record.get_floors_of_private_value(),
                    location_type=spot_record.get_location_type_of_private_value(),
                    latitude=coordinate_collection_select_record.get_coordinate_list_of_private_value()[
                        index
                    ].get_latitude_of_private_value(),
                    longitude=coordinate_collection_select_record.get_coordinate_list_of_private_value()[
                        index
                    ].get_longitude_of_private_value(),
                )
                for index, spot_record in enumerate(
                    spot_collection_select_record.get_spot_record_collection_of_private_value()
                )
            ]
        )

        return spot_collection
