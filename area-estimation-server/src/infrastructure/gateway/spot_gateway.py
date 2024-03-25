from typing import List, Optional

from psycopg2.extensions import connection

from infrastructure.record.spot_record import SpotCollectionRecord, SpotRecord


class SpotGateway:
    def find_by_spot_ids(
        self,
        conn: connection,
        spot_ids: List[str],
    ) -> Optional[SpotCollectionRecord]:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM spots WHERE id = ANY(%s)", (spot_ids,))

            spot_select_result = cursor.fetchall()
            if not spot_select_result:
                return None

            return SpotCollectionRecord(
                spot_record_collection=[
                    SpotRecord(
                        id=result[0],
                        name=result[1],
                        floors=result[2],
                        location_type=result[3],
                        created_at=result[4],
                    )
                    for result in spot_select_result
                ]
            )
