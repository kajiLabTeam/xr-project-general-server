from io import BytesIO
from typing import Any, List

import numpy as np
import pandas as pd
from config.const import EPSILON
from scipy import integrate  # type: ignore


class NormalDistributionComparator:
    def __init__(
        self,
        p_fp_model_file_bytes: bytes,
        q_fp_model_file_bytes: bytes,
    ) -> None:
        p_df = pd.read_csv(BytesIO(p_fp_model_file_bytes))  # type: ignore
        q_df = pd.read_csv(BytesIO(q_fp_model_file_bytes))  # type: ignore
        self.__p_mean_list: List[float] = p_df["mean"]  # type: ignore
        self.__p_std_list: List[float] = p_df["std"]  # type: ignore
        self.__q_mean_list: List[float] = q_df["mean"]  # type: ignore
        self.__q_std_list: List[float] = q_df["std"]  # type: ignore

    def __normal_pdf(self, x: Any, mean: float, std: float) -> Any:
        """
        正規分布の確率密度関数
        """
        result = (
            1
            / (np.sqrt(2 * np.pi * std**2))
            * np.exp(-((x - mean) ** 2) / (2 * std**2))
        )

        return np.maximum(result, EPSILON)

    def __kl_divergence(
        self,
        p_mean: float,
        p_std: float,
        q_mean: float,
        q_std: float,
    ) -> float:
        # KLダイバージェンスの被積分関数
        integrand = lambda x: self.__normal_pdf(x, p_mean, p_std) * np.log(  # type: ignore
            self.__normal_pdf(x, p_mean, p_std) / self.__normal_pdf(x, q_mean, q_std)
        )
        # KLダイバージェンスの計算
        # 被積分関数を p_mean - 5 * p_std から p_mean + 5 * p_std まで積分
        # 5をかけているのは、正規分布の確率密度関数は平均から標準偏差の5倍の範囲でほぼ0になるため
        kl_div, _ = integrate.quad(integrand, p_mean - 5 * p_std, p_mean + 5 * p_std)  # type: ignore

        return kl_div  # type: ignore

    def calculate_difference_of_normal_distribution(self) -> float:
        kl_div = 0
        for p_mean_list, p_std_list, q_mean_list, q_std_list in zip(
            self.__p_mean_list, self.__p_std_list, self.__q_mean_list, self.__q_std_list
        ):
            kl_div += self.__kl_divergence(
                p_mean_list, p_std_list, q_mean_list, q_std_list
            )
        return kl_div
