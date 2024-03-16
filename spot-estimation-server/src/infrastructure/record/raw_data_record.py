class RawDataRecord:
    def __init__(
        self,
        id: str,
        extension: str,
        spot_id: str,
        created_at: str,
    ) -> None:
        self.__id = id
        self.__extension = extension
        self.__spot_id = spot_id
        self.__created_at = created_at

    def get_id_of_private_value(self) -> str:
        return self.__id

    def get_spot_id_of_private_value(self) -> str:
        return self.__spot_id

    def get_extension_of_private_value(self) -> str:
        return self.__extension

    def get_created_at_of_private_value(self) -> str:
        return self.__created_at
