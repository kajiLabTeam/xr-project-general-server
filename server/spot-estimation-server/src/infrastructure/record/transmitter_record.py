from typing import List

from domain.models.transmitter.ble import Ble
from domain.models.transmitter.wifi import Wifi


class WifiRecord:
    def __init__(
        self,
        id: str,
        name: str,
        mac_address: str,
        rssi: float,
        created_at: str = "",
    ) -> None:
        self.__id = id
        self.__name = name
        self.__mac_address = mac_address
        self.__rssi = rssi
        self.__created_at = created_at

    def get_id_of_private_value(self) -> str:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_mac_address_of_private_value(self) -> str:
        return self.__mac_address

    def get_rssi_of_private_value(self) -> float:
        return self.__rssi

    def get_created_at_of_private_value(self) -> str:
        return self.__created_at


class BleRecord:
    def __init__(
        self,
        id: str,
        name: str,
        mac_address: str,
        rssi: float,
        created_at: str = "",
    ) -> None:
        self.__id = id
        self.__name = name
        self.__mac_address = mac_address
        self.__rssi = rssi
        self.__created_at = created_at

    def get_id_of_private_value(self) -> str:
        return self.__id

    def get_name_of_private_value(self) -> str:
        return self.__name

    def get_mac_address_of_private_value(self) -> str:
        return self.__mac_address

    def get_rssi_of_private_value(self) -> float:
        return self.__rssi

    def get_created_at_of_private_value(self) -> str:
        return self.__created_at


class TransmitterRecord:
    def __init__(
        self,
        ble_record_collection: List[BleRecord],
        wifi_record_collection: List[WifiRecord],
    ) -> None:
        self.__ble_record_collection = ble_record_collection
        self.__wifi_record_collection = wifi_record_collection

    def get_ble_record_collection_of_private_value(self) -> List[BleRecord]:
        return self.__ble_record_collection

    def get_wifi_record_collection_of_private_value(self) -> List[WifiRecord]:
        return self.__wifi_record_collection


class TransmitterRecordFactory:
    @staticmethod
    def create(
        ble_collection: List[Ble],
        wifi_collection: List[Wifi],
    ) -> TransmitterRecord:
        return TransmitterRecord(
            ble_record_collection=[
                BleRecord(
                    id=ble.get_id_of_private_value().get_id_of_private_value(),
                    name=ble.get_name_of_private_value(),
                    mac_address=ble.get_mac_address_of_private_value(),
                    rssi=ble.get_rssi_of_private_value(),
                )
                for ble in ble_collection
            ],
            wifi_record_collection=[
                WifiRecord(
                    id=wifi.get_id_of_private_value().get_id_of_private_value(),
                    name=wifi.get_name_of_private_value(),
                    mac_address=wifi.get_mac_address_private_value(),
                    rssi=wifi.get_rssi_private_value(),
                )
                for wifi in wifi_collection
            ],
        )
