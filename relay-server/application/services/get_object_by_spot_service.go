package services

import (
	"github.com/kajiLabTeam/xr-project-relay-server/config"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
)

type GetObjectBySpotService struct {
	objectRepo repository_impl.ObjectRepositoryImpl
	spotRepo   repository_impl.SpotRepositoryImpl
}

func NewGetObjectBySpotService(
	objectRepo repository_impl.ObjectRepositoryImpl,
	spotRepo repository_impl.SpotRepositoryImpl,
) *GetObjectBySpotService {
	return &GetObjectBySpotService{
		objectRepo: objectRepo,
		spotRepo:   spotRepo,
	}
}

func (goss *GetObjectBySpotService) Run(
	latitude float64,
	longitude float64,
	rawDataFile []byte,
	user *user_models_domain.User,
	application *application_models_domain.Application,
) (
	*user_models_domain.User,
	*object_models_domain.Object,
	*object_collection_models_domain.ObjectCollection,
	error,
) {
	// エリア探索を用いて周辺スポットを取得
	areaSpotCollection, err := goss.spotRepo.FindForCoordinateAndRadius(
		config.AREA_THRESHOLD,
		latitude,
		longitude,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// 周辺スポットがない場合
	if areaSpotCollection == nil {
		return user, nil, nil, nil
	}

	// 周辺スポットのIDを取得
	spotIds := areaSpotCollection.GetSpotIds()

	// 周辺スポットを元にスポットに紐づくオブジェクトを取得
	areaObject, err := goss.objectRepo.FindForSpotIds(
		spotIds,
		user,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// 周辺スポットに紐づくオブジェクトがない場合
	if areaObject == nil {
		return user, nil, nil, nil
	}

	areaObject.LinkSpots(areaSpotCollection)

	// 周辺スポットをヒントにピンポイントのスポットを取得
	spot, err := goss.spotRepo.FindForIdsAndRawDataFile(
		spotIds,
		rawDataFile,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// ピンポイントのスポットがない場合
	if spot == nil {
		return user, nil, nil, nil
	}

	// 屋内推定をしたユーザのピンポイントのスポットIDを取得
	spotId := spot.GetId()

	// ピンポイントのスポットを元にスポットに紐づくオブジェクトを取得
	spotObject, err := goss.objectRepo.FindForSpotId(
		spotId,
		user,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// ピンポイントのスポットに紐づくオブジェクトがない場合
	if spotObject == nil {
		return user, nil, nil, nil
	}

	spotObject.LinkSpot(spot)

	return user, spotObject, areaObject, nil
}
