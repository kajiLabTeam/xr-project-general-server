from typing import Any

from domain.models.application.aggregate import ApplicationAggregate
from domain.models.raw_data.aggregate import RawDataAggregate
from domain.models.spot.spot_id import SpotAggregateId
from domain.repository_impl.raw_data_repository_impl import \
    RawDataRepositoryImpl
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)
from infrastructure.gateway.raw_data_gateway import RawDataGateway
from psycopg2.extensions import connection

raw_data_gateway = RawDataGateway()


class RawDataRepository(RawDataRepositoryImpl):
    def find_for_spot_id(
        self,
        s3: Any,
        conn: connection,
        spot_id: SpotAggregateId,
        application: ApplicationAggregate,
    ) -> RawDataAggregate:
        with conn as conn:
            raw_data_record = raw_data_gateway.find_by_spot_id(
                conn=conn,
                spot_id=spot_id.get_id_of_private_value(),
            )
            if raw_data_record is None:
                raise InfrastructureError(
                    InfrastructureErrorType.RAW_DATA_IS_NOT_FOUND,
                    "Failed to find raw data",
                )

            key = (
                spot_id.get_id_of_private_value()
                + raw_data_record.get_extension_of_private_value()
            )
            raw_data_file = raw_data_gateway.download(
                s3=s3,
                key=key,
                application=application,
            )

            return RawDataAggregate(
                extension=raw_data_record.get_extension_of_private_value(),
                raw_data_file=raw_data_file,
            )

    def save(
        self,
        s3: Any,
        conn: connection,
        spot_id: SpotAggregateId,
        raw_data: RawDataAggregate,
        application: ApplicationAggregate,
    ) -> RawDataAggregate:
        with conn as conn:
            raw_data_insert_result = raw_data_gateway.save(
                conn=conn,
                raw_data_id=raw_data.get_id_private_value().get_id_of_private_value(),
                extension=raw_data.get_extension_private_value(),
                spot_id=spot_id.get_id_of_private_value(),
            )
            if raw_data_insert_result is None:
                raise InfrastructureError(
                    InfrastructureErrorType.RAW_DATA_INSERT_ERROR,
                    "Failed to insert raw data",
                )

            key = (
                spot_id.get_id_of_private_value()
                + "."
                + raw_data.get_extension_private_value()
            )
            raw_data_upload_result = raw_data_gateway.upload(
                s3=s3,
                key=key,
                raw_data_file=raw_data.get_raw_data_private_value(),
                application=application,
            )

            return RawDataAggregate(
                extension=raw_data.get_extension_private_value(),
                raw_data_file=raw_data_upload_result,
            )
