from utils.ulid import generate_ulid

APPLICATION_BUCKET_NAME: str = "applications"

BLE_NAME: str = "ble"
WIFI_NAME: str = "wifi"

TRANSMITTER_RSSI_THRESHOLD: int = -80
TRANSMITTER_THRESHOLD_NUMBER: int = 2
TRANSMITTER_ADDRESS_NUMBER_THRESHOLD: int = 4
TRANSMITTER_COINCIDENT_RATIO_THRESHOLD: float = 0.5
TRANSMITTER_NUMBER_DIFFERENCE_THRESHOLD: int = 1000000

RAW_DATA_EXTENSION: str = "csv"
RAW_DATA_FILE_BUCKET_NAME: str = "raw-data"


FP_MODEL_EXTENSION: str = "csv"
FP_MODEL_BUCKET_NAME: str = "fp-models"
FP_MODEL_STD_DEV_THRESHOLD: float = 1.0
FP_MODEL_LOSS_FUNCTION_VALUE_THRESHOLD: float = 1e-11
FP_MODEL_TEMPORARY_SAVING_PATH = "./" + str(generate_ulid()) + ".csv"


# 確率密度関数を生成するにあたり分母が0になった場合の値
EPSILON: float = 1e-10

# 標準偏差0を回避するための値
AVOID_ZERO_STD: float = 0.1
