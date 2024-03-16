package services

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
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
	latitude float64,
	longitude float64,
	user *user_models_domain.User,
	application *application_models_domain.Application,
) (
	*user_models_domain.User,
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
		return user, nil, err
	}
	// 周辺スポットがない場合
	if areaSpotCollection == nil {
		return user, nil, nil
	}

	// 周辺スポットのIDを取得
	spotIds := areaSpotCollection.GetSpotIds()

	// 周辺スポットを元にスポットに紐づくオブジェクトを取得
	areaObject, err := goas.objectRepo.FindForSpotIds(
		spotIds,
		user,
		application,
	)
	if err != nil {
		return user, nil, err
	}
	// 周辺スポットがない場合
	if areaObject == nil {
		return user, nil, nil
	}

	areaObject.LinkSpots(areaSpotCollection)

	return user, areaObject, nil

}
