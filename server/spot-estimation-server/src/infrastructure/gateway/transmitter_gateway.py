from typing import List, Optional

from infrastructure.record.transmitter_record import (BleRecord,
                                                      TransmitterRecord,
                                                      WifiRecord)
from psycopg2.extensions import connection


class TransmitterGateway:
    def find_by_spot_id(
        self, conn: connection, spot_id: str
    ) -> Optional[TransmitterRecord]:
        with conn.cursor() as cursor:
            # spot_idを元にwifiテーブルからwifiデータを取得
            cursor.execute(
                "SELECT * FROM wifis WHERE spot_id = %s",
                (spot_id,),
            )

            wifi_data = cursor.fetchall()

            # spot_idを元にbleテーブルからbleデータを取得
            cursor.execute(
                "SELECT * FROM bles WHERE spot_id = %s",
                (spot_id,),
            )

            ble_data = cursor.fetchall()

            if not wifi_data and not ble_data:
                return None

            wifi_collection = [
                WifiRecord(
                    id=wifi[0],
                    name=wifi[1],
                    mac_address=wifi[2],
                    rssi=wifi[3],
                )
                for wifi in wifi_data
            ]

            ble_collection = [
                BleRecord(
                    id=ble[0],
                    name=ble[1],
                    mac_address=ble[2],
                    rssi=ble[3],
                )
                for ble in ble_data
            ]

            return TransmitterRecord(
                ble_record_collection=ble_collection,
                wifi_record_collection=wifi_collection,
            )

    def save(
        self,
        conn: connection,
        spot_id: str,
        wifi_collection: List[WifiRecord],
        ble_collection: List[BleRecord],
    ) -> Optional[TransmitterRecord]:
        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO wifis (id, name, mac_address, rssi, spot_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, mac_address
                """,
                [
                    (
                        wifi.get_id_of_private_value(),
                        wifi.get_name_of_private_value(),
                        wifi.get_mac_address_of_private_value(),
                        wifi.get_rssi_of_private_value(),
                        spot_id,
                    )
                    for wifi in wifi_collection
                ],
            )

            cursor.executemany(
                """
                INSERT INTO bles (id, name, rssi, mac_address, spot_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, mac_address
                """,
                [
                    (
                        ble.get_id_of_private_value(),
                        ble.get_name_of_private_value(),
                        ble.get_rssi_of_private_value(),
                        ble.get_mac_address_of_private_value(),
                        spot_id,
                    )
                    for ble in ble_collection
                ],
            )

        return TransmitterRecord(
            ble_record_collection=ble_collection,
            wifi_record_collection=wifi_collection,
        )
