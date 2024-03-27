from utils.ulid import generate_ulid

APPLICATION_BUCKET_NAME: str = "applications"
FP_MODEL_BUCKET_NAME: str = "fp-models"
RAW_DATA_FILE_BUCKET_NAME: str = "raw-data"
TRANSMITTER_NUMBER_DIFFERENCE_THRESHOLD: int = 1000000
TRANSMITTER_THRESHOLD_NUMBER: int = 2
TRANSMITTER_COINCIDENT_RATIO_THRESHOLD: float = 0.9
FP_MODEL_TEMPORARY_SAVING_PATH = "./" + str(generate_ulid()) + ".csv"
FP_MODEL_STD_DEV_THRESHOLD: float = 1.0
FP_MODEL_LOSS_FUNCTION_VALUE_THRESHOLD: float = 160.0
FP_MODEL_EXTENSION: str = "csv"


RSSI_THRESHOLD: int = -80

ADDRESS_NUMBER_THRESHOLD: int = 4

# プロットされるグラフを表現する際の点の数
PLOT_NUMBER_POINT: int = 1000

# 確率密度関数を生成するにあたり分母が0になった場合の値
EPSILON: float = 1e-10

# 標準偏差0を回避するための値
AVOID_ZERO_STD: float = 0.1
