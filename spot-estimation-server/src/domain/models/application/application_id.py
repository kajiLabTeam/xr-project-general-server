class ApplicationId:
    def __init__(self, value: str):
        self.__value = value

    def get_id_of_private_value(self) -> str:
        return self.__value
