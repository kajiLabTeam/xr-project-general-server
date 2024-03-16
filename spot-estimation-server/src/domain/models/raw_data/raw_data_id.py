from utils.ulid import generate_ulid


class RawDataId:
    def __init__(self):
        self.id = generate_ulid()

    def get_id_of_private_value(self) -> str:
        return str(self.id)
