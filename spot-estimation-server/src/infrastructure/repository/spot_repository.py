from psycopg2.extensions import connection

from domain.models.spot.aggregate import SpotAggregate, SpotAggregateFactory
from domain.models.spot.spot_id import SpotAggregateId
from domain.repository_impl.spot_repository_impl import SpotRepositoryImpl
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)
from infrastructure.gateway.coordinate_gateway import CoordinateGateway
from infrastructure.gateway.spot_gateway import SpotGateway

spot_gateway = SpotGateway()
coordinate_gateway = CoordinateGateway()


class SpotRepository(SpotRepositoryImpl):
    def find_for_spot_id(
        self,
        conn: connection,
        spot_id: SpotAggregateId,
    ) -> SpotAggregate:
        with conn as conn:
            spot_record = spot_gateway.find_for_id(
                conn=conn,
                spot_id=spot_id.get_id_of_private_value(),
            )
            if spot_record is None:
                raise InfrastructureError(
                    InfrastructureErrorType.SPOT_IS_NOT_FOUND,
                    "Failed to find spot",
                )

            coordinate_record = coordinate_gateway.find_for_spot_id(
                conn=conn,
                spot_id=spot_id.get_id_of_private_value(),
            )
            if coordinate_record is None:
                raise InfrastructureError(
                    InfrastructureErrorType.COORDINATE_IS_NOT_FOUND,
                    "Failed to find coordinate",
                )

            return SpotAggregateFactory.create(
                id=spot_record.get_id_of_private_value(),
                name=spot_record.get_name_of_private_value(),
                floor=spot_record.get_floor_of_private_value(),
                location_type=spot_record.get_location_type_of_private_value(),
                latitude=coordinate_record.get_latitude_of_private_value(),
                longitude=coordinate_record.get_longitude_of_private_value(),
            )

    def save(
        self,
        conn: connection,
        spot: SpotAggregate,
    ) -> SpotAggregate:
        with conn as conn:
            spot_insert_result = spot_gateway.insert(
                conn=conn,
                id=spot.get_id_of_private_value().get_id_of_private_value(),
                name=spot.get_name_of_private_value(),
                floor=spot.get_floor_of_private_value(),
                location_type=spot.get_location_type_of_private_value().get_location_type_of_private_value(),
            )
            if spot_insert_result is None:
                raise InfrastructureError(
                    InfrastructureErrorType.SPOT_INSERT_ERROR,
                    "Error: SpotRepository.save",
                )

            coordinate_insert_result = coordinate_gateway.insert(
                conn=conn,
                coordinate_id=spot.get_coordinate_of_private_value().get_id_of_private_value(),
                latitude=spot.get_coordinate_of_private_value().get_latitude_of_private_value(),
                longitude=spot.get_coordinate_of_private_value().get_longitude_of_private_value(),
                spot_id=spot_insert_result.get_id_of_private_value(),
            )
            if coordinate_insert_result is None:
                raise InfrastructureError(
                    InfrastructureErrorType.COORDINATE_INSERT_ERROR,
                    "Error: SpotRepository.save",
                )

            return SpotAggregateFactory.create(
                id=coordinate_insert_result.get_spot_id_of_private_value(),
                name=spot.get_name_of_private_value(),
                floor=spot.get_floor_of_private_value(),
                location_type=spot.get_location_type_of_private_value().get_location_type_of_private_value(),
                latitude=coordinate_insert_result.get_latitude_of_private_value(),
                longitude=coordinate_insert_result.get_longitude_of_private_value(),
            )
