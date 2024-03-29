from collections import defaultdict
from typing import Dict, List

from config.const import TRANSMITTER_THRESHOLD_NUMBER
from domain.models.transmitter.ble_id import BleId


class Ble:
    def __init__(
        self,
        ssid: str,
        rssi: float,
        name: str = "",
    ):
        self.__id = BleId()
        self.__name = name
        self.__ssid = ssid
        self.__rssi = round(rssi, 2)

    def get_id_of_private_value(self) -> BleId:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_ssid_of_private_value(self) -> str:
        return self.__ssid

    def get_rssi_of_private_value(self) -> float:
        return self.__rssi


class BleCollection:
    def __init__(self, ble_list: List[Ble] = []):
        self.__ble_list = ble_list

    def get_ble_list_of_private_value(self) -> List[Ble]:
        return self.__ble_list

    def add_ble(self, ble: Ble):
        self.__ble_list.append(ble)

    def remove_ble(self, ble: Ble):
        self.__ble_list.remove(ble)

    def extract_id_ble_collection(self) -> List[BleId]:
        return [ble.get_id_of_private_value() for ble in self.__ble_list]

    # INFO : リクエストの度に同じIDを生成するので、IDを再生成する
    def re_typing_id(self):
        self.__ble_list = [
            Ble(
                ssid=ble.get_ssid_of_private_value(),
                rssi=ble.get_rssi_of_private_value(),
            )
            for ble in self.__ble_list
        ]

    # ssidの一致率を計測
    def measuring_match_rates(self, ble_collection: "BleCollection") -> float:
        # BLEのssid一致率を計測
        ble_ssids = [
            ble.get_ssid_of_private_value()
            for ble in self.get_ble_list_of_private_value()
        ]
        ble_ssid_match_count = sum(
            1
            for ble_ssid in ble_ssids
            if ble_ssid
            in [
                ble.get_ssid_of_private_value()
                for ble in ble_collection.get_ble_list_of_private_value()
            ]
        )
        ble_ssid_match_ratio = ble_ssid_match_count / max(len(ble_ssids), 1)

        return ble_ssid_match_ratio

    # 一定数以上のデータを残し、一意なSSIDでRSSIを平均化する
    def process_ble_collection(self) -> "BleCollection":
        ssid_rssi_mapping: Dict[str, List[float]] = defaultdict(list)

        # SSIDを元にRSSIをグループ化
        for ble in self.get_ble_list_of_private_value():
            ssid_rssi_mapping[ble.get_ssid_of_private_value()].append(
                ble.get_rssi_of_private_value()
            )

        processed_wifi_collection = BleCollection()
        for ssid, rssi_list in ssid_rssi_mapping.items():
            if len(rssi_list) > TRANSMITTER_THRESHOLD_NUMBER:  # 要素数が1つのものは削除
                avg_rssi = sum(rssi_list) / len(rssi_list)  # RSSIの平均値を計算
                processed_wifi_collection.add_ble(Ble(ssid=ssid, rssi=avg_rssi))

        return processed_wifi_collection
