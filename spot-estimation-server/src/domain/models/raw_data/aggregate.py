import csv
import re
from io import BytesIO
from os import remove
from typing import Tuple

import pandas as pd
from config.const import (FP_MODEL_EXTENSION, FP_MODEL_TEMPORARY_SAVING_PATH,
                          RAW_DATA_EXTENSION)
from domain.models.raw_data.raw_data_id import RawDataId
from domain.models.raw_data.statistical_analyzer import StatisticalAnalyzer
from domain.models.transmitter.ble import Ble, BleCollection
from domain.models.transmitter.wifi import Wifi, WifiCollection


class RawDataAggregate:
    def __init__(
        self,
        extension: str,
        raw_data_file: bytes,
    ):
        self.__id = RawDataId()
        self.__extension = extension
        self.__raw_data_file = raw_data_file

    def get_id_private_value(self) -> RawDataId:
        return self.__id

    def get_extension_private_value(self) -> str:
        return self.__extension

    def get_raw_data_private_value(self) -> bytes:
        return self.__raw_data_file

    def __generate_csv_bytes(self, data_frame: pd.DataFrame, file_path: str) -> bytes:
        data_frame.to_csv(file_path, index=False)
        with open(file_path, "rb") as file:
            csv_bytes = file.read()
        remove(file_path)

        return csv_bytes

    def __is_mac_address(self, mac_address: str) -> bool:
        # MACアドレスの正規表現パターン
        mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

        # パターンに一致するかどうかを判定
        return bool(mac_pattern.match(mac_address))

    # 生データからBLEとWIFIの発信機情報を抽出
    def extract_transmitter(self) -> Tuple[BleCollection, WifiCollection]:
        bytes_io = BytesIO(self.__raw_data_file)
        csv_reader = csv.reader(bytes_io.read().decode("utf-8").splitlines())
        ble_collection = BleCollection()
        wifi_collection = WifiCollection()

        # ヘッダーをスキップ
        next(csv_reader, None)

        # 1行ずつ読み込む
        for row in csv_reader:
            if len(row) == 3:
                rssi = int(row[1])
                address = row[2]

                if self.__is_mac_address(address):
                    wifi_collection.add_wifi(
                        Wifi(ssid="", rssi=rssi, mac_address=address)
                    )
                else:
                    ble_collection.add_ble(Ble(ssid=address, rssi=rssi))

        return (
            ble_collection.process_ble_collection(),
            wifi_collection.process_wifi_collection(),
        )

    def generate_fp_model(self) -> Tuple[bytes, str]:
        """
        正規分布を作成するため平均と標準偏差を含むFPモデルを生成
        """
        raw_data_bytes = BytesIO(self.__raw_data_file)
        static_analyzer = StatisticalAnalyzer(raw_data_bytes=raw_data_bytes)

        return (
            self.__generate_csv_bytes(
                data_frame=static_analyzer.get_mean_and_std_df(),
                file_path=FP_MODEL_TEMPORARY_SAVING_PATH,
            ),
            FP_MODEL_EXTENSION,
        )


class RawDataAggregateFactory:
    @staticmethod
    def create(
        raw_data_file: bytes,
    ) -> RawDataAggregate:
        return RawDataAggregate(
            raw_data_file=raw_data_file,
            extension=RAW_DATA_EXTENSION,
        )
