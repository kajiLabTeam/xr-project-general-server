from domain.error.domain_error import DomainError, DomainErrorType


class LocationType:
    def __init__(
        self,
        location_type: str,
    ) -> None:
        if location_type not in ["indoor", "outdoor"]:
            raise DomainError(
                type=DomainErrorType.INVALID_LOCATION,
                message=f"location_type is invalid: {location_type}",
            )
        self.__location_type = location_type

    def get_location_type_of_private_value(self) -> str:
        return self.__location_type
