from collections import defaultdict
from typing import Dict, List, Optional

import numpy as np
from config.const import TRANSMITTER_THRESHOLD_NUMBER
from domain.models.transmitter.ble_id import BleId


class Ble:
    def __init__(
        self,
        rssi: float,
        mac_address: str,
        name: Optional[str] = "",
    ):
        self.__id = BleId()
        self.__name = name if name is not None else ""
        self.__rssi = round(rssi, 2)
        self.__mac_address = mac_address

    def get_id_of_private_value(self) -> BleId:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_rssi_of_private_value(self) -> float:
        return self.__rssi

    def get_mac_address_of_private_value(self) -> str:
        return self.__mac_address


class BleCollection:
    def __init__(self, ble_list: Optional[List[Ble]] = None):
        self.__ble_list = ble_list if ble_list is not None else []

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
                rssi=ble.get_rssi_of_private_value(),
                mac_address=ble.get_mac_address_of_private_value(),
            )
            for ble in self.__ble_list
        ]

    # mac_addressの一致率を計測
    def measuring_match_rates(self, ble_collection: "BleCollection") -> float:
        # BLEのmac_addressを集合に変換
        ble_mac_addresses_set = {
            ble.get_mac_address_of_private_value()
            for ble in self.get_ble_list_of_private_value()
        }

        # 比較対象のBLEコレクションのmac_addressを集合に変換
        compare_mac_addresses_set = {
            ble.get_mac_address_of_private_value()
            for ble in ble_collection.get_ble_list_of_private_value()
        }

        # 一致するmac_addressの数を計算
        match_count = len(ble_mac_addresses_set.intersection(compare_mac_addresses_set))

        # mac_addressの数を取得
        total_mac_addresses = max(len(ble_mac_addresses_set), 1)

        # 一致率を計算
        match_ratio = match_count / total_mac_addresses

        return match_ratio

    # 一定数以上のデータを残し、一意なmac_addressでRSSIを平均化する
    def process_ble_collection(self) -> "BleCollection":
        mac_address_rssi_mapping: Dict[str, List[float]] = defaultdict(list)

        # mac_addressを元にRSSIをグループ化
        for ble in self.get_ble_list_of_private_value():
            mac_address_rssi_mapping[ble.get_mac_address_of_private_value()].append(
                ble.get_rssi_of_private_value()
            )

        processed_ble_collection = BleCollection()
        for mac_address, rssi_list in mac_address_rssi_mapping.items():
            if len(rssi_list) > TRANSMITTER_THRESHOLD_NUMBER:  # 要素数が1つのものは削除
                avg_rssi = np.mean(rssi_list)
                processed_ble_collection.add_ble(Ble(mac_address=mac_address, rssi=avg_rssi))  # type: ignore

        return processed_ble_collection
