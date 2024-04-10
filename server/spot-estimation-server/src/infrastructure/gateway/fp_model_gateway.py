from io import BytesIO
from typing import Any, Optional

import psycopg2.sql as sql
from config.const import APPLICATION_BUCKET_NAME, FP_MODEL_BUCKET_NAME
from domain.models.application.aggregate import ApplicationAggregate
from infrastructure.record.fp_model_record import FpModelRecord
from psycopg2.extensions import connection


class FpModelGateway:
    def find_by_spot_id(
        self, conn: connection, spot_id: str
    ) -> Optional[FpModelRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT * FROM fp_models WHERE spot_id = %s"),
                (spot_id,),
            )

            data = cursor.fetchone()
            if data is None:
                return None

            cursor.close()

            return FpModelRecord(
                id=data[0],
                extension=data[1],
                spot_id=data[5],
            )

    def save(
        self,
        conn: connection,
        fp_model_id: str,
        extension: str,
        spot_id: str,
    ) -> Optional[FpModelRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    """
                    INSERT INTO fp_models (id, extension, spot_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, extension, spot_id
                    """
                ),
                (fp_model_id, extension, spot_id),
            )
            inserted_data = cursor.fetchone()
            if inserted_data is None:
                return None

            cursor.close()

            return FpModelRecord(
                id=inserted_data[0],
                extension=inserted_data[1],
                spot_id=inserted_data[2],
            )

    def download(self, s3: Any, key: str, application: ApplicationAggregate) -> bytes:
        key = f"{application.get_id_of_private_value()}/{FP_MODEL_BUCKET_NAME}/{key}"
        obj = s3.get_object(Bucket=APPLICATION_BUCKET_NAME, Key=key)
        return obj["Body"].read()

    def upload(
        self,
        s3: Any,
        key: str,
        fp_model_file: bytes,
        application: ApplicationAggregate,
    ) -> bytes:
        buffer = BytesIO(fp_model_file)
        key = f"{application.get_id_of_private_value()}/{FP_MODEL_BUCKET_NAME}/{key}"

        s3.upload_fileobj(buffer, APPLICATION_BUCKET_NAME, key)
        buffer.close()

        return fp_model_file
