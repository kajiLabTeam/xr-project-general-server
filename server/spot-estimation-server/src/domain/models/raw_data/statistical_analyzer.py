from io import BytesIO

import numpy as np
import pandas as pd
from config.const import (AVOID_ZERO_STD, TRANSMITTER_RSSI_THRESHOLD,
                          WIFI_MAC_ADDRESS_NUMBER_THRESHOLD)


class StatisticalAnalyzer:
    def __init__(self, raw_data_bytes: BytesIO) -> None:
        self.__raw_data_df = pd.read_csv(raw_data_bytes).drop(columns=["gets"])  # type: ignore

    def __based_on_rssi(self) -> None:
        """
        rssiが閾値以下のデータはDFから削除
        """
        self.__raw_data_df = self.__raw_data_df[
            self.__raw_data_df["rssi"] >= TRANSMITTER_RSSI_THRESHOLD
        ]

    def __unique_by_rssi_threshold(self) -> None:
        """
        rssiの出現回数の閾値を元にaddressを一意にする
        """
        counts_raw_data_df_by_address = (  # type: ignore
            self.__raw_data_df.groupby("address").size().reset_index(name="count")  # type: ignore
        )
        self.__raw_data_df = self.__raw_data_df.merge(  # type: ignore
            counts_raw_data_df_by_address, on="address"
        )
        self.__raw_data_df = self.__raw_data_df[
            self.__raw_data_df["count"] >= WIFI_MAC_ADDRESS_NUMBER_THRESHOLD
        ]
        self.__raw_data_df.drop("count", axis=1, inplace=True)  # type: ignore

    def get_mean_and_std_df(self) -> pd.DataFrame:
        """
        データフレームから平均と標準偏差のリストを取得
        """
        self.__based_on_rssi()
        self.__unique_by_rssi_threshold()

        # 平均と標準偏差を導出
        mean_std_df = (
            self.__raw_data_df.groupby(["address", "type"])["rssi"]  # type: ignore
            .agg(["mean", "std"])
            .reset_index()
        )
        mean_std_df["std"] = np.where(
            mean_std_df["std"] == 0, AVOID_ZERO_STD, mean_std_df["std"]  # type: ignore
        )

        return mean_std_df
