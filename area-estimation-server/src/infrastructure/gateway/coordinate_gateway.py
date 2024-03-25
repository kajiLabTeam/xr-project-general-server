from typing import List, Optional

import psycopg2.sql as sql
from psycopg2.extensions import connection

from infrastructure.record.coordinate_record import (
    CoordinateCollectionRecord, CoordinateRecord)


class CoordinateGateway:
    def find_for_coordinates(
        self,
        conn: connection,
        center_latitude: float,
        center_longitude: float,
        circumferential_latitude_list: List[float],
        circumferential_longitude_list: List[float],
    ) -> Optional[CoordinateCollectionRecord]:
        with conn.cursor() as cursor:
            coordinate_record_list = CoordinateCollectionRecord([])

            for circumferential_latitude, circumferential_longitude in zip(
                circumferential_latitude_list, circumferential_longitude_list
            ):
                # SQLクエリの構築
                query = sql.SQL(
                    """
                    SELECT *
                    FROM coordinates
                    WHERE 
                        latitude BETWEEN {} AND {}
                        AND longitude BETWEEN {} AND {}
                    """
                ).format(
                    sql.Literal(min(center_latitude, circumferential_latitude)),
                    sql.Literal(max(center_latitude, circumferential_latitude)),
                    sql.Literal(min(center_longitude, circumferential_longitude)),
                    sql.Literal(max(center_longitude, circumferential_longitude)),
                )

                cursor.execute(query)

                results = cursor.fetchall()
                if not results:
                    return None

                for result in results:
                    coordinate_record_list.add_coordinate(
                        CoordinateRecord(
                            id=result[0],
                            latitude=result[1],
                            longitude=result[2],
                            spot_id=result[3],
                        )
                    )

            return coordinate_record_list.unique_coordinate()
