from utils.ulid import generate_ulid

APPLICATION_BUCKET_NAME: str = "applications"
FP_MODEL_BUCKET_NAME: str = "fp-models"
RAW_DATA_FILE_BUCKET_NAME: str = "raw-data"
TRANSMITTER_THRESHOLD_NUMBER: int = 2
TRANSMITTER_COINCIDENT_RATIO_THRESHOLD: float = 0.9
FP_MODEL_TEMPORARY_SAVING_PATH = "./" + str(generate_ulid()) + ".csv"
FP_MODEL_STD_DEV_THRESHOLD: float = 1.0
FP_MODEL_COINCIDENT_RATIO_THRESHOLD: float = 0.9
