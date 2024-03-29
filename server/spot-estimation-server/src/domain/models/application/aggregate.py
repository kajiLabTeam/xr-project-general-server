from domain.models.application.application_id import ApplicationId


class ApplicationAggregate:
    def __init__(self, id: str, secret_key: str) -> None:
        self.__id = ApplicationId(id)
        self.__secret_key = secret_key

    def get_id_of_private_value(self) -> str:
        return self.__id.get_id_of_private_value()

    def get_secret_key_of_private_value(self) -> str:
        return self.__secret_key
