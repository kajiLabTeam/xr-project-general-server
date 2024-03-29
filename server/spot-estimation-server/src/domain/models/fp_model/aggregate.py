from domain.error.domain_error import DomainError, DomainErrorType
from domain.models.fp_model.fp_model_id import FpModelAggregateId
from domain.models.fp_model.normal_distribution_comparator import \
    NormalDistributionComparator
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

    def calculate_loss_function_value(self, fp_model: "FpModelAggregate") -> float:
        normal_distribution_comparator = NormalDistributionComparator(
            self.__fp_model_file, fp_model.__fp_model_file
        )

        loss_function_value = (
            normal_distribution_comparator.calculate_difference_of_normal_distribution()
        )

        return loss_function_value


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
