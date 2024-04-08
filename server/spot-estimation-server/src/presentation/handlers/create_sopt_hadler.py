from typing import Annotated, Tuple

from application.services.create_spot_service import CreateSpotService
from domain.models.application.aggregate import ApplicationAggregate
from domain.models.raw_data.aggregate import RawDataAggregateFactory
from domain.models.spot.aggregate import SpotAggregateFactory
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from infrastructure.repository.fp_model_repository import FpModelRepository
from infrastructure.repository.raw_data_repository import RawDataRepository
from infrastructure.repository.spot_repository import SpotRepository
from infrastructure.repository.transmitter_repository import \
    TransmitterRepository
from presentation.middleware.application_middleware import get_credential
from pydantic import BaseModel


class CreateSpotResponse(BaseModel):
    id: str
    name: str
    floor: int
    locationType: str
    latitude: float
    longitude: float


router = APIRouter()


create_spot_service = CreateSpotService(
    spot_repository=SpotRepository(),
    raw_data_repository=RawDataRepository(),
    fp_model_repository=FpModelRepository(),
    transmitter_repository=TransmitterRepository(),
)


@router.post("/api/spot/create", response_model=CreateSpotResponse, status_code=201)
async def create_spot(
    name: Annotated[str, Form()],
    floor: Annotated[int, Form()],
    locationType: Annotated[str, Form()],
    latitude: Annotated[float, Form()],
    longitude: Annotated[float, Form()],
    rawDataFile: Annotated[UploadFile, File()],
    credentials: Annotated[Tuple[str, str], Depends(get_credential)],
):
    try:
        raw_data_file = await rawDataFile.read()

        raw_data = RawDataAggregateFactory.create(
            raw_data_file=raw_data_file,
        )

        spot_aggregate = SpotAggregateFactory.create(
            name=name,
            floor=floor,
            location_type=locationType,
            latitude=latitude,
            longitude=longitude,
        )

        application_id, secret_key = credentials
        application = ApplicationAggregate(application_id, secret_key)

        # スポット情報を保存
        create_spot_service.run(
            raw_data=raw_data,
            spot=spot_aggregate,
            application=application,
        )

        return CreateSpotResponse(
            id=spot_aggregate.get_id_of_private_value().get_id_of_private_value(),
            name=spot_aggregate.get_name_of_private_value(),
            floor=spot_aggregate.get_floor_of_private_value(),
            locationType=spot_aggregate.get_location_type_of_private_value().get_location_type_of_private_value(),
            latitude=spot_aggregate.get_coordinate_of_private_value().get_latitude_of_private_value(),
            longitude=spot_aggregate.get_coordinate_of_private_value().get_longitude_of_private_value(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
