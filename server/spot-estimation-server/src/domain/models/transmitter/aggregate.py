from typing import List

from config.const import TRANSMITTER_COINCIDENT_RATIO_THRESHOLD
from domain.models.raw_data.aggregate import RawDataAggregate
from domain.models.transmitter.ble import Ble, BleCollection
from domain.models.transmitter.ble_id import BleId
from domain.models.transmitter.wifi import Wifi, WifiCollection
from domain.models.transmitter.wifi_id import WifiId


class TransmitterAggregate:
    def __init__(
        self,
        ble_collection: BleCollection,
        wifi_collection: WifiCollection,
    ):
        self.__ble_collection = ble_collection
        self.__wifi_collection = wifi_collection

    def get_ble_collection_of_private_value(self) -> List[Ble]:
        return self.__ble_collection.get_ble_list_of_private_value()

    def get_wifi_collection_of_private_value(self) -> List[Wifi]:
        return self.__wifi_collection.get_wifi_list_of_private_value()

    def extract_id_ble_collection(self) -> List[BleId]:
        return [
            ble.get_id_of_private_value()
            for ble in self.__ble_collection.get_ble_list_of_private_value()
        ]

    def extract_id_wifi_collection(self) -> List[WifiId]:
        return [
            wifi.get_id_of_private_value()
            for wifi in self.__wifi_collection.get_wifi_list_of_private_value()
        ]

    def is_match_connection(self, transmitter: "TransmitterAggregate") -> bool:
        """
        BLEの場合はssid、WIFIの場合はmac_addressの一致率を計測, そして閾値を超えたらTrueを返す
        """
        # BLEのssid一致率を計測
        ble_ssid_match_ratio = self.__ble_collection.measuring_match_rates(
            transmitter.__ble_collection
        )

        # WiFiのmac_address一致率を計測
        wifi_mac_match_ratio = self.__wifi_collection.measuring_match_rates(
            transmitter.__wifi_collection
        )

        print(f"BLEのssid一致率: {ble_ssid_match_ratio}")
        print(f"WIFIのmac_address一致率: {wifi_mac_match_ratio}")

        # BLEのssidとWiFiのmac_addressの一致率を結合して合計を計算
        total_match_ratio = (ble_ssid_match_ratio + wifi_mac_match_ratio) / 2

        # 合計が閾値を超えたらTrueを返す
        return total_match_ratio >= TRANSMITTER_COINCIDENT_RATIO_THRESHOLD


class TransmitterAggregateFactory:
    @staticmethod
    def create(
        raw_data: RawDataAggregate,
    ) -> TransmitterAggregate:
        ble_collection, wifi_collection = raw_data.extract_transmitter()

        wifi_collection.re_typing_id()
        ble_collection.re_typing_id()

        return TransmitterAggregate(
            ble_collection=ble_collection,
            wifi_collection=wifi_collection,
        )


class TransmitterAggregateInfrastructureFactory:
    @staticmethod
    def create(
        ble_collection: List[Ble],
        wifi_collection: List[Wifi],
    ) -> TransmitterAggregate:
        return TransmitterAggregate(
            ble_collection=BleCollection(ble_collection),
            wifi_collection=WifiCollection(wifi_collection),
        )
