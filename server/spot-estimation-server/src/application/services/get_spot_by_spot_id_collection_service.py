from typing import List, Optional

from domain.models.application.aggregate import ApplicationAggregate
from domain.models.fp_model.aggregate import FpModelAggregateFactory
from domain.models.raw_data.aggregate import RawDataAggregate
from domain.models.spot.aggregate import SpotAggregate
from domain.models.spot_collection.aggregate import SpotCollectionAggregate
from domain.models.transmitter.aggregate import TransmitterAggregateFactory
from domain.repository_impl.fp_model_repository_impl import \
    FpModelRepositoryImpl
from domain.repository_impl.spot_repository_impl import SpotRepositoryImpl
from domain.repository_impl.transmitter_repository_impl import \
    TransmitterRepositoryImpl
from infrastructure.connection import DBConnection, MinioConnection


class GetSpotBySpotIdCollectionService:
    def __init__(
        self,
        spot_repository: SpotRepositoryImpl,
        fp_model_repository: FpModelRepositoryImpl,
        transmitter_repository: TransmitterRepositoryImpl,
    ):
        self.__spot_repository = spot_repository
        self.__fp_model_repository = fp_model_repository
        self.__transmitter_repository = transmitter_repository

    def run(
        self,
        raw_data: RawDataAggregate,
        application: ApplicationAggregate,
        spot_collection: SpotCollectionAggregate,
    ) -> Optional[List[SpotAggregate]]:
        conn = DBConnection().connect()
        s3 = MinioConnection().connect()

        # 生データからFPモデルを生成
        current_fp_model = FpModelAggregateFactory.create(
            raw_data=raw_data,
        )
        # 生データから接続中の発信機情報を抽出
        connecting_transmitter = TransmitterAggregateFactory.create(
            raw_data=raw_data,
        )

        # 発信機情報を元にスポットを特定する
        spot_collection.identify_spot_by_transmitter(
            conn=conn,
            connecting_transmitter=connecting_transmitter,
            transmitter_repository=self.__transmitter_repository,
        )

        # スポットが特定できなかった場合
        if len(spot_collection.get_id_collection_of_private_value()) == 0:
            return None

        # FPモデルを元にスポットを一意に特定する
        spot_collection.identify_spot_by_fp_model(
            s3=s3,
            conn=conn,
            current_fp_model=current_fp_model,
            application=application,
            fp_model_repository=self.__fp_model_repository,
        )

        spot_list = spot_collection.generate_spot_aggregate_list(
            conn=conn,
            spot_repository=self.__spot_repository,
        )

        if len(spot_list) == 0:
            return None

        return spot_list
