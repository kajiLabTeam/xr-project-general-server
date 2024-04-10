from typing import Any

from domain.models.application.aggregate import ApplicationAggregate
from domain.models.fp_model.aggregate import FpModelAggregate
from domain.models.spot.spot_id import SpotAggregateId
from domain.repository_impl.fp_model_repository_impl import \
    FpModelRepositoryImpl
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)
from infrastructure.gateway.fp_model_gateway import FpModelGateway
from psycopg2.extensions import connection

fp_model_gateway = FpModelGateway()


class FpModelRepository(FpModelRepositoryImpl):
    def find_for_spot_id(
        self,
        s3: Any,
        conn: connection,
        spot_id: SpotAggregateId,
        application: ApplicationAggregate,
    ) -> FpModelAggregate:
        with conn as conn:
            try:
                fp_model_record = fp_model_gateway.find_by_spot_id(
                    conn=conn, spot_id=spot_id.get_id_of_private_value()
                )
                if fp_model_record is None:
                    raise InfrastructureError(
                        InfrastructureErrorType.FP_MODEL_IS_NOT_FOUND,
                        "Failed to find fp model",
                    )

                # minioに登録されたファイルを取得するためのファイル名を宣言
                key = (
                    fp_model_record.get_id_of_private_value()
                    + "."
                    + fp_model_record.get_extension_of_private_value()
                )

                # minioからファイルを取得
                fp_model = fp_model_gateway.download(
                    s3=s3, key=key, application=application
                )
            except InfrastructureError as err:
                raise InfrastructureError(
                    InfrastructureErrorType.FP_MODEL_IS_NOT_FOUND,
                    "Failed to download fp model",
                ) from err

            return FpModelAggregate(
                fp_model_file=fp_model,
                extension=fp_model_record.get_extension_of_private_value(),
            )

    def save(
        self,
        s3: Any,
        conn: connection,
        spot_id: SpotAggregateId,
        fp_model: FpModelAggregate,
        application: ApplicationAggregate,
    ) -> FpModelAggregate:
        with conn as conn:
            try:
                # FPモデルをDBに保存
                fp_model_insert_result = fp_model_gateway.save(
                    conn=conn,
                    fp_model_id=fp_model.get_id_of_private_value().get_id_of_private_value(),
                    extension=fp_model.get_extension_of_private_value(),
                    spot_id=spot_id.get_id_of_private_value(),
                )
                if fp_model_insert_result is None:
                    raise Exception("Failed to save raw data")

                # minioにアップロードするためのファイル名を宣言
                key = (
                    fp_model_insert_result.get_id_of_private_value()
                    + "."
                    + fp_model.get_extension_of_private_value()
                )
                # minioにファイルをアップロード
                fp_model_upload_result = fp_model_gateway.upload(
                    s3=s3,
                    key=key,
                    fp_model_file=fp_model.get_fp_model_of_private_value(),
                    application=application,
                )

                return FpModelAggregate(
                    fp_model_file=fp_model_upload_result,
                    extension=fp_model.get_extension_of_private_value(),
                )
            except InfrastructureError as err:
                raise InfrastructureError(
                    InfrastructureErrorType.FP_MODEL_IS_NOT_FOUND,
                    "Failed to download fp model",
                ) from err
