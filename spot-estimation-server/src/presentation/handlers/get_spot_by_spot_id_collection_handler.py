from typing import Annotated, List, Tuple

from application.services.get_spot_by_spot_id_collection_service import \
    GetSpotBySpotIdCollectionService
from domain.models.application.aggregate import ApplicationAggregate
from domain.models.raw_data.aggregate import RawDataAggregateFactory
from domain.models.spot_collection.aggregate import \
    SpotCollectionAggregateFactory
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from infrastructure.repository.fp_model_repository import FpModelRepository
from infrastructure.repository.spot_repository import SpotRepository
from infrastructure.repository.transmitter_repository import \
    TransmitterRepository
from presentation.middleware.application_middleware import get_credential
from pydantic import BaseModel


class SpotItem(BaseModel):
    id: str
    name: str
    floor: int
    locationType: str
    latitude: float
    longitude: float


class GetSpotBySpotIdCollectionResponse(BaseModel):
    spots: List[SpotItem]


router = APIRouter()

get_spot_by_spot_id_collection_service = GetSpotBySpotIdCollectionService(
    spot_repository=SpotRepository(),
    fp_model_repository=FpModelRepository(),
    transmitter_repository=TransmitterRepository(),
)


@router.post("/api/spot/search", response_model=GetSpotBySpotIdCollectionResponse)
async def get_spot_by_spot_id_collection(
    spotIds: Annotated[List[str], Query()],
    rawDataFile: Annotated[UploadFile, File()],
    credentials: Annotated[Tuple[str, str], Depends(get_credential)],
):
    try:
        spot_collection = SpotCollectionAggregateFactory().create(
            spot_id_collection=spotIds
        )

        raw_data_file = await rawDataFile.read()
        raw_data = RawDataAggregateFactory().create(
            raw_data_file=raw_data_file,
        )

        application_id, secret_key = credentials
        application = ApplicationAggregate(application_id, secret_key)

        spot_list = get_spot_by_spot_id_collection_service.run(
            raw_data=raw_data,
            application=application,
            spot_collection=spot_collection,
        )

        if spot_list is None:
            JSONResponse(
                status_code=404,
                content=GetSpotBySpotIdCollectionResponse(
                    spots=[],
                ),
            )
            return

        return GetSpotBySpotIdCollectionResponse(
            spots=[
                SpotItem(
                    id=spot.get_id_of_private_value().get_id_of_private_value(),
                    name=spot.get_name_of_private_value(),
                    floor=spot.get_floor_of_private_value(),
                    locationType=spot.get_location_type_of_private_value().get_location_type_of_private_value(),
                    latitude=spot.get_coordinate_of_private_value().get_latitude_of_private_value(),
                    longitude=spot.get_coordinate_of_private_value().get_longitude_of_private_value(),
                )
                for spot in spot_list
            ]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
