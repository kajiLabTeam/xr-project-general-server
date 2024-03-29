from domain.models.application.aggregate import ApplicationAggregate
from domain.models.fp_model.aggregate import FpModelAggregateFactory
from domain.models.raw_data.aggregate import RawDataAggregate
from domain.models.spot.aggregate import SpotAggregate
from domain.models.transmitter.aggregate import TransmitterAggregateFactory
from domain.repository_impl.fp_model_repository_impl import \
    FpModelRepositoryImpl
from domain.repository_impl.raw_data_repository_impl import \
    RawDataRepositoryImpl
from domain.repository_impl.spot_repository_impl import SpotRepositoryImpl
from domain.repository_impl.transmitter_repository_impl import \
    TransmitterRepositoryImpl
from infrastructure.connection import DBConnection, MinioConnection


class CreateSpotService:
    def __init__(
        self,
        spot_repository: SpotRepositoryImpl,
        raw_data_repository: RawDataRepositoryImpl,
        fp_model_repository: FpModelRepositoryImpl,
        transmitter_repository: TransmitterRepositoryImpl,
    ):
        self.__spot_repository = spot_repository
        self.__raw_data_repository = raw_data_repository
        self.__fp_model_repository = fp_model_repository
        self.__transmitter_repository = transmitter_repository

    def run(
        self,
        spot: SpotAggregate,
        raw_data: RawDataAggregate,
        application: ApplicationAggregate,
    ) -> SpotAggregate:
        conn = DBConnection().connect()
        s3 = MinioConnection().connect()

        # スポットIDは外部キーとして使用されるため、スポットIDを取得
        spot_id = spot.get_id_of_private_value()

        # 生データからFPモデルを生成
        fp_model = FpModelAggregateFactory.create(
            raw_data=raw_data,
        )
        # 生データから接続中の発信機情報を抽出
        transmitter = TransmitterAggregateFactory.create(
            raw_data=raw_data,
        )

        # スポット及びスポットに紐づく座標情報を保存
        spot = self.__spot_repository.save(
            conn=conn,
            spot=spot,
        )
        # 生データを保存
        raw_data = self.__raw_data_repository.save(
            s3=s3,
            conn=conn,
            spot_id=spot_id,
            raw_data=raw_data,
            application=application,
        )
        # FPモデルを保存
        fp_model = self.__fp_model_repository.save(
            conn=conn,
            s3=s3,
            spot_id=spot_id,
            fp_model=fp_model,
            application=application,
        )

        # 発信機情報を保存
        transmitter = self.__transmitter_repository.save(
            conn=conn,
            spot_id=spot_id,
            transmitter=transmitter,
        )

        # スポットに紐づく情報をリンクさせる
        spot.link_to_aggregate_fp_model(fp_model.get_id_of_private_value())
        spot.link_to_aggregate_transmitter(transmitter)

        return spot
