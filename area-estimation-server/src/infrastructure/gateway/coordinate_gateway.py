from typing import List, Optional

import psycopg2.sql as sql
from infrastructure.record.coordinate_record import (
    CoordinateCollectionRecord, CoordinateRecord)
from psycopg2.extensions import connection


class CoordinateGateway:
    def find_for_coordinates(
        self,
        conn: connection,
        latitudes: List[float],
        longitudes: List[float],
    ) -> Optional[CoordinateCollectionRecord]:
        with conn.cursor() as cursor:
            # SQLクエリの構築
            query = sql.SQL(
                "SELECT * FROM coordinates WHERE (latitude, longitude) IN ({})"
            ).format(
                sql.SQL(", ").join(
                    [
                        sql.Literal((latitude, longitude))
                        for latitude, longitude in zip(latitudes, longitudes)
                    ]
                )
            )

            cursor.execute(query)

            results = cursor.fetchall()
            if not results:
                return None

            return CoordinateCollectionRecord(
                coordinates=[
                    CoordinateRecord(
                        id=result[0],
                        latitude=result[1],
                        longitude=result[2],
                        spot_id=result[3],
                    )
                    for result in results
                ]
            )
