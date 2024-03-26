from typing import List, Optional

import psycopg2.sql as sql
from infrastructure.record.coordinate_record import (
    CoordinateCollectionRecord, CoordinateRecord)
from psycopg2.extensions import connection


class CoordinateGateway:
    def find_for_coordinate_list(
        self,
        conn: connection,
        center_latitude: float,
        center_longitude: float,
        circumferential_latitude_list: List[float],
        circumferential_longitude_list: List[float],
    ) -> Optional[CoordinateCollectionRecord]:
        with conn.cursor() as cursor:
            coordinate_collection_record = CoordinateCollectionRecord([])

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
                    continue

                for result in results:
                    coordinate_collection_record.add_coordinate(
                        CoordinateRecord(
                            id=result[0],
                            latitude=result[1],
                            longitude=result[2],
                            spot_id=result[3],
                        )
                    )

        if (
            len(coordinate_collection_record.get_coordinate_list_of_private_value())
            == 0
        ):
            return None

        # 重複を削除
        coordinate_collection_record.unique_coordinate()

        return coordinate_collection_record
