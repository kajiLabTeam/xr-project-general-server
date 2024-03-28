from io import BytesIO

import pandas as pd
from config.const import (AVOID_ZERO_STD, TRANSMITTER_ADDRESS_NUMBER_THRESHOLD,
                          TRANSMITTER_RSSI_THRESHOLD)


class StatisticalAnalyzer:
    def __init__(self, raw_data_bytes: BytesIO) -> None:
        self.__raw_data_df = pd.read_csv(raw_data_bytes).drop(columns=["gets"])  # type: ignore

    # rssiが閾値以下のデータはDFから削除
    def __based_on_rssi(self) -> None:
        self.__raw_data_df = self.__raw_data_df[
            self.__raw_data_df["rssi"] >= TRANSMITTER_RSSI_THRESHOLD
        ]

    # rssiの出現回数の閾値を元にaddressを一意にする
    def __unique_by_rssi_threshold(self) -> None:
        # addressをグループ化し、各グループのサイズ（出現回数）をカウント
        counts_raw_data_df_by_address = self.__raw_data_df.groupby("address").size().reset_index(name="count")  # type: ignore

        self.__raw_data_df = pd.merge(  # type: ignore
            self.__raw_data_df, counts_raw_data_df_by_address, on="address"
        )

        # 'address' の出現回数が閾値以下の行を削除
        self.__raw_data_df = self.__raw_data_df[
            self.__raw_data_df["count"] >= TRANSMITTER_ADDRESS_NUMBER_THRESHOLD
        ]

        self.__raw_data_df = self.__raw_data_df.drop("count", axis=1)  # type: ignore

    # データフレームから平均と標準偏差のリストを取得
    def get_mean_and_std_df(
        self,
    ) -> pd.DataFrame:
        self.__based_on_rssi()
        self.__unique_by_rssi_threshold()

        # 平均と標準偏差を導出
        mean_std_df = (
            self.__raw_data_df.groupby("address")["rssi"]  # type: ignore
            .agg(["mean", "std"])
            .reset_index()
        )

        # 標準偏差が0の場合はあらかじめ決めた値にする
        mean_std_df["std"] = mean_std_df["std"].apply(lambda x: AVOID_ZERO_STD if x == 0 else x)  # type: ignore

        return mean_std_df
