from typing import Any, List

from config.const import FP_MODEL_LOSS_FUNCTION_VALUE_THRESHOLD
from domain.error.domain_error import DomainError, DomainErrorType
from domain.models.application.aggregate import ApplicationAggregate
from domain.models.fp_model.aggregate import FpModelAggregate
from domain.models.spot.aggregate import SpotAggregate
from domain.models.spot.spot_id import SpotAggregateId
from domain.models.spot_collection.spot_collection_id import SpotCollectionId
from domain.models.transmitter.aggregate import TransmitterAggregate
from domain.repository_impl.fp_model_repository_impl import \
    FpModelRepositoryImpl
from domain.repository_impl.spot_repository_impl import SpotRepositoryImpl
from domain.repository_impl.transmitter_repository_impl import \
    TransmitterRepositoryImpl
from infrastructure.error.infrastructure_error import InfrastructureError
from psycopg2.extensions import connection
from ulid import ULID


class SpotCollectionAggregate:
    def __init__(
        self,
        spot_id_collection: List[SpotAggregateId],
    ):
        self.__id = SpotCollectionId()
        self.__spot_id_collection: List[SpotAggregateId] = spot_id_collection

    def get_id_of_private_value(self) -> SpotCollectionId:
        return self.__id

    def get_id_collection_of_private_value(self) -> List[SpotAggregateId]:
        return self.__spot_id_collection

    def add_spot_id(self, spot_id: SpotAggregateId):
        self.__spot_id_collection.append(spot_id)

    # spot_id_collectionからスポットIDを削除
    def remove_spot_id(self, spot_id: SpotAggregateId):
        self.__spot_id_collection = [
            id_ for id_ in self.__spot_id_collection if id_ != spot_id
        ]

    def generate_spot_aggregate_list(
        self,
        conn: connection,
        spot_repository: SpotRepositoryImpl,
    ) -> List[SpotAggregate]:
        spot_aggregate_list: List[SpotAggregate] = []
        for spot_id in self.__spot_id_collection:
            try:  # スポットIDが存在しない場合はスキップ
                spot_aggregate = spot_repository.find_for_spot_id(
                    conn=conn, spot_id=spot_id
                )
                spot_aggregate_list.append(spot_aggregate)
            except InfrastructureError:
                continue
        return spot_aggregate_list

    # 発信機情報を元にスポットを特定する
    def identify_spot_by_transmitter(
        self,
        conn: connection,
        connecting_transmitter: TransmitterAggregate,
        transmitter_repository: TransmitterRepositoryImpl,
    ):
        # スポットIDの集約から発信機情報と一致しないスポットIDを削除
        for spot_id in self.__spot_id_collection:
            try:
                # 人がいる候補となるスポットの発信機情報を取得
                candidate_transmitter = transmitter_repository.find_for_spot_id(
                    conn=conn,
                    spot_id=spot_id,
                )

                # 発信機の一致率が閾値を超えていない場合、スポットIDの集約から削除
                if not candidate_transmitter.is_match_connection(
                    transmitter=connecting_transmitter
                ):
                    self.remove_spot_id(spot_id)
            except InfrastructureError:
                self.remove_spot_id(spot_id)
                continue

    def identify_spot_by_fp_model(
        self,
        s3: Any,
        conn: connection,
        application: ApplicationAggregate,
        current_fp_model: FpModelAggregate,
        fp_model_repository: FpModelRepositoryImpl,
    ):
        """
        FPモデルを元にスポットを絞り込む
        """
        # スポットIDの集約から発信機情報と一致しないスポットIDを削除
        for spot_id in self.__spot_id_collection:
            try:
                # 人がいる候補となるスポットのFPモデルを取得
                candidate_fp_model = fp_model_repository.find_for_spot_id(
                    conn=conn,
                    s3=s3,
                    spot_id=spot_id,
                    application=application,
                )

                # 2つのFPモデルの損失関数の値を計算
                loss_function_value = current_fp_model.calculate_loss_function_value(
                    fp_model=candidate_fp_model
                )

                print("FPモデルの損失関数の値", loss_function_value)

                # 一致率が閾値を超えていない場合、スポットIDの集約から削除
                if loss_function_value > FP_MODEL_LOSS_FUNCTION_VALUE_THRESHOLD:
                    self.remove_spot_id(spot_id=spot_id)
            except InfrastructureError:
                self.remove_spot_id(spot_id)
                continue


class SpotCollectionAggregateFactory:
    @staticmethod
    def create(spot_id_collection: List[str]) -> SpotCollectionAggregate:
        ulid_collection: List[ULID] = []
        for spot_id in spot_id_collection:
            try:
                uuid = ULID.from_str(spot_id)
                ulid_collection.append(uuid)
            except ValueError:
                raise DomainError(
                    DomainErrorType.INVALID_ULID,
                    "Invalid spot id",
                )

        return SpotCollectionAggregate(
            spot_id_collection=[SpotAggregateId(ulid) for ulid in ulid_collection]
        )
