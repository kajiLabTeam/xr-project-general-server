from typing import List, Optional

from infrastructure.record.transmitter_record import (BleRecord,
                                                      TransmitterRecord,
                                                      WifiRecord)
from psycopg2.extensions import connection
from utils.ulid import generate_ulid


class TransmitterGateway:
    def find_by_spot_id(
        self, conn: connection, spot_id: str
    ) -> Optional[TransmitterRecord]:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT array_agg(wifi_id) FROM spots_wifis WHERE spot_id = %s",
                (spot_id,),
            )
            wifi_ids = cursor.fetchall()[0][0]

            # 中間テーブルからspot_idに紐づくble_idを取得
            cursor.execute(
                "SELECT array_agg(ble_id) FROM spots_bles WHERE spot_id = %s",
                (spot_id,),
            )
            ble_ids = cursor.fetchall()[0][0]

            if not wifi_ids and not ble_ids:
                return None

            # wifi_idsを元にwifiテーブルからwifiデータを取得
            cursor.execute(
                "SELECT * FROM wifis WHERE id = ANY(%s)",
                ([wifi_id for wifi_id in wifi_ids],),
            )

            wifi_data = cursor.fetchall()

            # ble_idsを元にbleテーブルからbleデータを取得
            cursor.execute(
                "SELECT * FROM bles WHERE id = ANY(%s)",
                ([ble_id for ble_id in ble_ids],),
            )

            ble_data = cursor.fetchall()

            if not wifi_data and not ble_data:
                return None

            wifi_collection = [
                WifiRecord(
                    id=wifi[0],
                    name=wifi[1],
                    ssid=wifi[2],
                    rssi=wifi[4],
                    mac_address=wifi[3],
                )
                for wifi in wifi_data
            ]

            ble_collection = [
                BleRecord(
                    id=ble[0],
                    name=ble[1],
                    ssid=ble[2],
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
                "INSERT INTO wifis (id, name, ssid, mac_address, rssi) VALUES (%s, %s, %s, %s, %s) RETURNING id, name, ssid, mac_address",
                [
                    (
                        wifi.get_id_of_private_value(),
                        wifi.get_name_of_private_value(),
                        wifi.get_ssid_of_private_value(),
                        wifi.get_mac_address_of_private_value(),
                        wifi.get_rssi_of_private_value(),
                    )
                    for wifi in wifi_collection
                ],
            )

            cursor.executemany(
                "INSERT INTO spots_wifis (id, spot_id, wifi_id) VALUES (%s, %s, %s)",
                [
                    (
                        str(generate_ulid()),
                        spot_id,
                        wifi.get_id_of_private_value(),
                    )
                    for wifi in wifi_collection
                ],
            )

            cursor.executemany(
                "INSERT INTO bles (id, name, ssid) VALUES (%s, %s, %s) RETURNING id, name, ssid",
                [
                    (
                        ble.get_id_of_private_value(),
                        ble.get_name_of_private_value(),
                        ble.get_ssid_of_private_value(),
                    )
                    for ble in ble_collection
                ],
            )

            cursor.executemany(
                "INSERT INTO spots_bles (id, spot_id, ble_id) VALUES (%s, %s, %s)",
                [
                    (
                        str(generate_ulid()),
                        spot_id,
                        ble.get_id_of_private_value(),
                    )
                    for ble in ble_collection
                ],
            )

        return TransmitterRecord(
            ble_record_collection=ble_collection,
            wifi_record_collection=wifi_collection,
        )
