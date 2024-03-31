from typing import List

from domain.models.spot.spot_id import SpotAggregateId
from domain.models.transmitter.aggregate import (
    TransmitterAggregate, TransmitterAggregateInfrastructureFactory)
from domain.models.transmitter.ble import Ble
from domain.models.transmitter.wifi import Wifi
from domain.repository_impl.transmitter_repository_impl import \
    TransmitterRepositoryImpl
from infrastructure.error.infrastructure_error import (InfrastructureError,
                                                       InfrastructureErrorType)
from infrastructure.gateway.transmitter_gateway import TransmitterGateway
from infrastructure.record.transmitter_record import TransmitterRecordFactory
from psycopg2.extensions import connection

transmitter_gateway = TransmitterGateway()


class TransmitterRepository(TransmitterRepositoryImpl):
    def find_for_spot_id(
        self,
        conn: connection,
        spot_id: SpotAggregateId,
    ) -> TransmitterAggregate:
        with conn as conn:
            transmitter_record = transmitter_gateway.find_by_spot_id(
                conn=conn,
                spot_id=spot_id.get_id_of_private_value(),
            )
            if transmitter_record is None:
                raise InfrastructureError(
                    InfrastructureErrorType.TRANSMITTER_IS_NOT_FOUND,
                    "Failed to find transmitter",
                )

            ble_collection: List[Ble] = [
                Ble(
                    ssid=ble_record.get_ssid_of_private_value(),
                    name=ble_record.get_name_of_private_value(),
                    rssi=ble_record.get_rssi_of_private_value(),
                )
                for ble_record in transmitter_record.get_ble_record_collection_of_private_value()
            ]
            wifi_collection: List[Wifi] = [
                Wifi(
                    name=wifi_record.get_name_of_private_value(),
                    ssid=wifi_record.get_ssid_of_private_value(),
                    mac_address=wifi_record.get_mac_address_of_private_value(),
                    rssi=wifi_record.get_rssi_of_private_value(),
                )
                for wifi_record in transmitter_record.get_wifi_record_collection_of_private_value()
            ]

            return TransmitterAggregateInfrastructureFactory.create(
                ble_collection=ble_collection,
                wifi_collection=wifi_collection,
            )

    def save(
        self,
        conn: connection,
        spot_id: SpotAggregateId,
        transmitter: TransmitterAggregate,
    ) -> TransmitterAggregate:
        with conn as conn:
            transmitter_record = TransmitterRecordFactory.create(
                transmitter.get_ble_collection_of_private_value(),
                transmitter.get_wifi_collection_of_private_value(),
            )

            transmitter_insert_result = transmitter_gateway.save(
                conn=conn,
                spot_id=spot_id.get_id_of_private_value(),
                ble_collection=transmitter_record.get_ble_record_collection_of_private_value(),
                wifi_collection=transmitter_record.get_wifi_record_collection_of_private_value(),
            )
            if transmitter_insert_result is None:
                raise InfrastructureError(
                    InfrastructureErrorType.TRANSMITTER_INSERT_ERROR,
                    "Failed to save transmitter",
                )

            # TODO: 保存したデータを取得して返す
            return transmitter
