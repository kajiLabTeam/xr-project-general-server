package services

import (
	"github.com/kajiLabTeam/xr-project-relay-server/config"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
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
	*object_collection_models_domain.ObjectCollection,
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
	areaSpotIds := areaSpotCollection.GetSpotIds()

	// 周辺スポットを元にスポットに紐づくオブジェクトを取得
	areaObject, err := goss.objectRepo.FindForSpotIds(
		areaSpotIds,
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
	spots, err := goss.spotRepo.FindForIdsAndRawDataFile(
		areaSpotIds,
		rawDataFile,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// ピンポイントのスポットがない場合
	if spots == nil {
		return user, nil, nil, nil
	}

	// 屋内推定をしたユーザのピンポイントのスポットIDを取得
	spotIds := spots.GetSpotIds()

	// ピンポイントのスポットを元にスポットに紐づくオブジェクトを取得
	spotObjects, err := goss.objectRepo.FindForSpotIds(
		spotIds,
		user,
		application,
	)
	if err != nil {
		return user, nil, nil, err
	}
	// ピンポイントのスポットに紐づくオブジェクトがない場合
	if spotObjects == nil {
		return user, nil, nil, nil
	}

	spotObjects.LinkSpots(spots)

	return user, spotObjects, areaObject, nil
}
