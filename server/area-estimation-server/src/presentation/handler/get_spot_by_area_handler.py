from typing import List

from application.service.get_spot_by_area_service import \
    GetSpotCollectionByAreaService
from domain.model.area.aggregate import AreaAggregateFactory
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from infrastructure.repository.spot_collection_repository import \
    SpotCollectionRepository
from pydantic import BaseModel

router = APIRouter()

get_spot_collection_by_area_service = GetSpotCollectionByAreaService(
    spot_collection_repository=SpotCollectionRepository()
)


class GetSpotCollectionByAreaRequest(BaseModel):
    latitude: float
    longitude: float


class SpotItem(BaseModel):
    id: str
    name: str
    floors: int
    locationType: str
    latitude: float
    longitude: float


class GetSpotCollectionByAreaResponse(BaseModel):
    spots: List[SpotItem]


@router.post("/api/area/search", response_model=GetSpotCollectionByAreaResponse)
async def get_spot_by_spot_id_collection(
    radius: int, request: GetSpotCollectionByAreaRequest
):
    try:
        # リクエストボディから値を取得
        latitude = request.latitude
        longitude = request.longitude

        area = AreaAggregateFactory.create(
            radius=radius,
            latitude=latitude,
            longitude=longitude,
        )

        # サービスを実行
        spot_collection = get_spot_collection_by_area_service.run(area=area)

        if spot_collection is None:
            return JSONResponse(
                status_code=404,
                content={"spots": []},
            )

        # レスポンスボディを作成
        response = GetSpotCollectionByAreaResponse(
            spots=[
                SpotItem(
                    id=str(spot.get_id_of_private_value().get_id_of_private_value()),
                    name=spot.get_name_of_private_value(),
                    floors=spot.get_floors_of_private_value(),
                    locationType=spot.get_location_type_of_private_value().get_location_type_of_private_value(),
                    latitude=spot.get_coordinate_of_private_value().get_latitude_of_private_value(),
                    longitude=spot.get_coordinate_of_private_value().get_longitude_of_private_value(),
                )
                for spot in spot_collection.get_spot_collection_of_private_value()
            ]
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
