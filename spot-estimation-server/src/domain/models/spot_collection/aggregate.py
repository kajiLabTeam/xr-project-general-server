from typing import Any, List

from config.const import FP_MODEL_COINCIDENT_RATIO_THRESHOLD
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

    def remove_spot_id(self, spot_id: SpotAggregateId):
        self.__spot_id_collection.remove(spot_id)

    def generate_spot_aggregate_list(
        self,
        conn: connection,
        spot_repository: SpotRepositoryImpl,
    ) -> List[SpotAggregate]:
        spot_aggregate_list: List[SpotAggregate] = []
        for spot_id in self.__spot_id_collection:
            spot_aggregate = spot_repository.find_for_spot_id(
                conn=conn, spot_id=spot_id
            )
            spot_aggregate_list.append(spot_aggregate)
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

    # INFO : 現在使われていません
    # DBに登録されているFPモデルのうち、最も近しいスポットを一意に特定する
    def identify_spot_by_fp_model_uniquely(
        self,
        s3: Any,
        conn: connection,
        application: ApplicationAggregate,
        current_fp_model: FpModelAggregate,
        fp_model_repository: FpModelRepositoryImpl,
    ):
        max_agreement = 0.0
        # スポットIDの集約から発信機情報と一致しないスポットIDを削除
        for spot_id in self.__spot_id_collection:
            # 人がいる候補となるスポットのFPモデルを取得
            candidate_fp_model = fp_model_repository.find_for_spot_id(
                conn=conn,
                s3=s3,
                spot_id=spot_id,
                application=application,
            )

            agreement_percentage = current_fp_model.calculate_percentage_of_agreement(
                fp_model=candidate_fp_model
            )

            if agreement_percentage > max_agreement:
                max_agreement = agreement_percentage
            else:
                self.remove_spot_id(spot_id)

    def identify_spot_by_fp_model(
        self,
        s3: Any,
        conn: connection,
        application: ApplicationAggregate,
        current_fp_model: FpModelAggregate,
        fp_model_repository: FpModelRepositoryImpl,
    ):
        # スポットIDの集約から発信機情報と一致しないスポットIDを削除
        for spot_id in self.__spot_id_collection:
            # 人がいる候補となるスポットのFPモデルを取得
            candidate_fp_model = fp_model_repository.find_for_spot_id(
                conn=conn,
                s3=s3,
                spot_id=spot_id,
                application=application,
            )

            # FPモデルの一致率を計算
            agreement_percentage = current_fp_model.calculate_percentage_of_agreement(
                fp_model=candidate_fp_model
            )

            # 一致率が閾値を超えていない場合、スポットIDの集約から削除
            if agreement_percentage < FP_MODEL_COINCIDENT_RATIO_THRESHOLD:
                self.remove_spot_id(spot_id=spot_id)


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
