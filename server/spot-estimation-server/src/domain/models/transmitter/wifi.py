from collections import defaultdict
from typing import Dict, List, Optional

import numpy as np
from config.const import TRANSMITTER_THRESHOLD_NUMBER
from domain.models.transmitter.wifi_id import WifiId


class Wifi:
    def __init__(
        self,
        rssi: float,
        mac_address: str,
        name: Optional[str] = None,
    ):
        self.__id = WifiId()
        self.__name = name if name is not None else ""
        self.__rssi = round(rssi, 2)
        self.__mac_address = mac_address

    def get_id_of_private_value(self) -> WifiId:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_rssi_private_value(self) -> float:
        return self.__rssi

    def get_mac_address_of_private_value(self) -> str:
        return self.__mac_address


class WifiCollection:
    def __init__(self, wifi_list: Optional[List[Wifi]] = None):
        self.__wifi_list = wifi_list if wifi_list is not None else []

    def get_wifi_list_of_private_value(self) -> List[Wifi]:
        return self.__wifi_list

    def add_wifi(self, wifi: Wifi):
        self.__wifi_list.append(wifi)

    def remove_wifi(self, wifi: Wifi):
        self.__wifi_list.remove(wifi)

    def extract_id_wifi_collection(self) -> List[WifiId]:
        return [wifi.get_id_of_private_value() for wifi in self.__wifi_list]

    # mac_addressの一致率を計測
    def measuring_match_rates(self, wifi_collection: "WifiCollection") -> float:
        # WiFiのMACアドレスを集合に変換
        wifi_mac_address_set = {
            wifi.get_mac_address_of_private_value()
            for wifi in self.get_wifi_list_of_private_value()
        }

        # 比較対象のWiFiコレクションのMACアドレスを集合に変換
        compare_mac_addresses_set = {
            wifi.get_mac_address_of_private_value()
            for wifi in wifi_collection.get_wifi_list_of_private_value()
        }

        # 一致するMACアドレスの数を計算
        match_count = len(wifi_mac_address_set.intersection(compare_mac_addresses_set))

        # MACアドレスの数を取得
        total_mac_addresses = max(len(wifi_mac_address_set), 1)

        # 一致率を計算
        match_ratio = match_count / total_mac_addresses

        return match_ratio

    # 一定数以上のデータを残し、一意なmac_addressでRSSIを平均化する
    def process_wifi_collection(self) -> "WifiCollection":
        # for wifi in self.get_wifi_list_of_private_value():
        #     print(f"MACアドレス: {wifi.get_mac_address_of_private_value()}")
        #     print(f"RSSI: {wifi.get_rssi_private_value()}")
        mac_address_rssi_mapping: Dict[str, List[float]] = defaultdict(list)

        # mac_addressを元にRSSIをグループ化
        for wifi in self.get_wifi_list_of_private_value():
            mac_address_rssi_mapping[wifi.get_mac_address_of_private_value()].append(
                wifi.get_rssi_private_value()
            )

        processed_wifi_collection = WifiCollection()
        for mac_address, rssi_list in mac_address_rssi_mapping.items():
            if len(rssi_list) > TRANSMITTER_THRESHOLD_NUMBER:  # 要素数が1つのものは削除
                avg_rssi = np.mean(rssi_list)  # RSSIの平均値を計算
                processed_wifi_collection.add_wifi(
                    Wifi(mac_address=mac_address, rssi=avg_rssi)  # type: ignore
                )

        for wifi in processed_wifi_collection.get_wifi_list_of_private_value():
            print(f"MACアドレス: {wifi.get_mac_address_of_private_value()}")

        return processed_wifi_collection
