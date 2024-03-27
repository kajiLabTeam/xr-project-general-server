package services

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
)

type GetObjectByAreaService struct {
	objectRepo repository_impl.ObjectRepositoryImpl
	spotRepo   repository_impl.SpotRepositoryImpl
}

func NewGetObjectByAreaService(
	objectRepo repository_impl.ObjectRepositoryImpl,
	spotRepo repository_impl.SpotRepositoryImpl,
) *GetObjectByAreaService {
	return &GetObjectByAreaService{
		objectRepo: objectRepo,
		spotRepo:   spotRepo,
	}
}

func (goas *GetObjectByAreaService) Run(
	area int,
	userId string,
	latitude float64,
	longitude float64,
	application *application_models_domain.Application,
) (
	*string,
	*object_collection_models_domain.ObjectCollection,
	error,
) {
	// エリア探索を用いて周辺スポットを取得
	areaSpotCollection, err := goas.spotRepo.FindForCoordinateAndRadius(
		area,
		latitude,
		longitude,
		application,
	)
	if err != nil {
		return nil, nil, err
	}
	// 周辺スポットがない場合
	if areaSpotCollection == nil {
		return &userId, nil, nil
	}

	// 周辺スポットのIDを取得
	spotIds := areaSpotCollection.GetSpotIds()

	// 周辺スポットを元にスポットに紐づくオブジェクトを取得
	areaObject, err := goas.objectRepo.FindForSpotIds(
		userId,
		spotIds,
		application,
	)
	if err != nil {
		return &userId, nil, err
	}
	// 周辺スポットがない場合
	if areaObject == nil {
		return &userId, nil, nil
	}

	areaObject.LinkSpots(areaSpotCollection)

	return &userId, areaObject, nil

}
