from typing import List, Optional

from infrastructure.record.spot_record import SpotCollectionRecord, SpotRecord
from psycopg2.extensions import connection


class SpotGateway:
    def find_for_id(
        self,
        conn: connection,
        spot_id: str,
    ) -> Optional[SpotRecord]:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM spots WHERE id = %s", (spot_id,))
            spot_select_result = cursor.fetchone()
            if spot_select_result is None:
                return None

            return SpotRecord(
                id=spot_select_result[0],
                name=spot_select_result[1],
                floor=spot_select_result[2],
                location_type=spot_select_result[3],
                created_at=spot_select_result[4],
            )

    def find_by_ids(
        self,
        conn: connection,
        spot_ids: List[str],
    ) -> Optional[SpotCollectionRecord]:
        with conn.cursor() as cursor:
            # spot_idのリストを元にspotテーブルからspotデータを取得
            cursor.execute("SELECT * FROM spots WHERE id = ANY(%s)", (spot_ids,))
            spot_select_result = cursor.fetchall()
            if not spot_select_result:
                return None

            return SpotCollectionRecord(
                spot_record_collection=[
                    SpotRecord(
                        id=result[0],
                        name=result[1],
                        floor=result[2],
                        location_type=result[3],
                        created_at=result[4],
                    )
                    for result in spot_select_result
                ]
            )

    def insert(
        self,
        conn: connection,
        id: str,
        name: str,
        floor: int,
        location_type: str,
    ) -> Optional[SpotRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO spots (id, name, floor, location_type) VALUES (%s, %s, %s, %s) RETURNING id, name, floor, location_type, created_at",
                (
                    id,
                    name,
                    floor,
                    location_type,
                ),
            )

            inserted_data = cursor.fetchone()

            if inserted_data is None:
                return None

            return SpotRecord(
                id=inserted_data[0],
                name=inserted_data[1],
                floor=inserted_data[2],
                location_type=inserted_data[3],
                created_at=inserted_data[4],
            )
