from io import BytesIO
from typing import Any, Optional

import psycopg2.sql as sql
from config.const import APPLICATION_BUCKET_NAME, RAW_DATA_FILE_BUCKET_NAME
from domain.models.application.aggregate import ApplicationAggregate
from infrastructure.record.raw_data_record import RawDataRecord
from psycopg2.extensions import connection


class RawDataGateway:
    def find_by_spot_id(
        self,
        conn: connection,
        spot_id: str,
    ) -> Optional[RawDataRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT * FROM raw_data WHERE spot_id = %s"), (spot_id,)
            )

            data = cursor.fetchone()
            if data is None:
                return None

            return RawDataRecord(
                id=data[0],
                extension=data[1],
                spot_id=data[2],
                created_at=data[3],
            )

    def save(
        self, conn: connection, raw_data_id: str, extension: str, spot_id: str
    ) -> Optional[RawDataRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    """
                    INSERT INTO raw_data (id, extension, spot_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, extension, spot_id, created_at
                    """
                ),
                (raw_data_id, extension, spot_id),
            )
            inserted_data = cursor.fetchone()
            if inserted_data is None:
                return None

            return RawDataRecord(
                id=inserted_data[0],
                extension=inserted_data[1],
                spot_id=inserted_data[2],
                created_at=inserted_data[3],
            )

    def download(self, s3: Any, key: str, application: ApplicationAggregate) -> bytes:
        key = (
            f"{application.get_id_of_private_value()}/{RAW_DATA_FILE_BUCKET_NAME}/{key}"
        )
        obj = s3.get_object(Bucket=APPLICATION_BUCKET_NAME, Key=key)
        return obj["Body"].read()

    def upload(
        self,
        s3: Any,
        key: str,
        raw_data_file: bytes,
        application: ApplicationAggregate,
    ) -> bytes:
        buffer = BytesIO(raw_data_file)
        key = (
            f"{application.get_id_of_private_value()}/{RAW_DATA_FILE_BUCKET_NAME}/{key}"
        )

        s3.upload_fileobj(buffer, APPLICATION_BUCKET_NAME, key)
        buffer.close()

        return raw_data_file
