from io import BytesIO

import numpy as np
import pandas as pd

from config.const import FP_MODEL_STD_DEV_THRESHOLD
from domain.error.domain_error import DomainError, DomainErrorType
from domain.models.fp_model.fp_model_id import FpModelAggregateId
from domain.models.raw_data.aggregate import RawDataAggregate


class FpModelAggregate:
    def __init__(
        self,
        fp_model_file: bytes,
        extension: str,
    ):
        if len(extension) > 10:
            raise DomainError(
                DomainErrorType.INVALID_FP_MODEL_EXTENSION,
                "Invalid extension",
            )
        self.__id = FpModelAggregateId()
        self.__fp_model_file = fp_model_file
        self.__extension = extension

    def get_id_of_private_value(self) -> FpModelAggregateId:
        return self.__id

    def get_fp_model_of_private_value(self) -> bytes:
        return self.__fp_model_file

    def get_extension_of_private_value(self) -> str:
        return self.__extension

    # TODO : FPモデルの一致率を計算する処理を実装する
    def calculate_percentage_of_agreement(self, fp_model: "FpModelAggregate") -> float:
        bytes_io_self = BytesIO(self.__fp_model_file)
        bytes_io_compared = BytesIO(fp_model.get_fp_model_of_private_value())

        data_self = pd.read_csv(bytes_io_self.read().decode("utf-8"))  # type: ignore
        data_compared = pd.read_csv(bytes_io_compared.read().decode("utf-8"))  # type: ignore
        # "address" 列が一致する行をマージ
        merged_data = pd.merge(  # type: ignore
            data_self,
            data_compared,
            on="address",
            suffixes=("_file_self", "_file_compared"),
        )

        # "std_dev" 列の差を計算
        merged_data["std_dev_diff"] = np.abs(
            merged_data["std_dev_file_self"] - merged_data["std_dev_file_compared"]  # type: ignore
        )

        # "std_dev_diff" が一定範囲内の行を抽出
        matching_rows = merged_data[
            merged_data["std_dev_diff"] <= FP_MODEL_STD_DEV_THRESHOLD
        ]

        # 一致率を計算して正規化
        matching_percentage = len(matching_rows) / len(data_self)
        matching_percentage_normalized = min(1.0, matching_percentage)  # 1.0 を上限に正規化
        return matching_percentage_normalized


class FpModelAggregateFactory:
    @staticmethod
    def create(
        raw_data: RawDataAggregate,
    ) -> FpModelAggregate:
        fp_model_file, extension = raw_data.generate_fp_model()

        return FpModelAggregate(
            fp_model_file=fp_model_file,
            extension=extension,
        )
