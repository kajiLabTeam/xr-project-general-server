from typing import List, Optional

import psycopg2.sql as sql
from infrastructure.record.coordinate_record import (
    CoordinateCollectionRecord, CoordinateRecord)
from psycopg2.extensions import connection


class CoordinateGateway:
    def find_for_spot_id(
        self,
        conn: connection,
        spot_id: str,
    ) -> Optional[CoordinateRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM coordinates WHERE spot_id = %s",
                (spot_id,),
            )

            results = cursor.fetchall()
            if not results:
                return None

            return CoordinateRecord(
                id=results[0][0],
                latitude=results[0][1],
                longitude=results[0][2],
                spot_id=results[0][3],
            )

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

    def insert(
        self,
        conn: connection,
        coordinate_id: str,
        latitude: float,
        longitude: float,
        spot_id: str,
    ) -> Optional[CoordinateRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO coordinates (id, latitude, longitude, spot_id) VALUES (%s, %s, %s, %s) RETURNING *",
                (
                    coordinate_id,
                    latitude,
                    longitude,
                    spot_id,
                ),
            )

            inserted_data = cursor.fetchone()
            if inserted_data is None:
                return None

            return CoordinateRecord(
                id=inserted_data[0],
                latitude=inserted_data[1],
                longitude=inserted_data[2],
                spot_id=inserted_data[3],
            )
