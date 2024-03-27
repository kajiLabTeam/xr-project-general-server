package services

import (
	"github.com/kajiLabTeam/xr-project-relay-server/config"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
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
	userId string,
	latitude float64,
	longitude float64,
	rawDataFile []byte,
	application *application_models_domain.Application,
) (
	*string,
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
		return nil, nil, nil, err
	}
	// 周辺スポットがない場合
	if areaSpotCollection == nil {
		return nil, nil, nil, nil
	}

	// 周辺スポットのIDを取得
	areaSpotIds := areaSpotCollection.GetSpotIds()

	// 周辺スポットを元にスポットに紐づくオブジェクトを取得
	areaObjects, err := goss.objectRepo.FindForSpotIds(
		userId,
		areaSpotIds,
		application,
	)
	if err != nil {
		return &userId, nil, nil, err
	}
	// 周辺スポットに紐づくオブジェクトがない場合
	if areaObjects == nil {
		return &userId, nil, nil, nil
	}

	// オブジェクト構造体にスポット構造体をリンク
	areaObjects.LinkSpots(areaSpotCollection)

	// 周辺スポットをヒントにピンポイントのスポットを取得
	spots, err := goss.spotRepo.FindForIdsAndRawDataFile(
		areaSpotIds,
		rawDataFile,
		application,
	)
	if err != nil {
		return &userId, nil, nil, err
	}
	// ピンポイントのスポットがない場合
	if spots == nil {
		return &userId, nil, areaObjects, nil
	}

	// 屋内推定をしたユーザのピンポイントのスポットIDを取得
	spotIds := spots.GetSpotIds()

	// ピンポイントのスポットを元にスポットに紐づくオブジェクトを取得
	spotObjects, err := goss.objectRepo.FindForSpotIds(
		userId,
		spotIds,
		application,
	)
	if err != nil {
		return &userId, nil, nil, err
	}
	// ピンポイントのスポットに紐づくオブジェクトがない場合
	if spotObjects == nil {
		return &userId, nil, areaObjects, nil
	}

	// areaObjectsに存在するspotObjectsとの重複を削除
	areaObjects.RemoveObjectByIds(spotObjects.GetObjectIds())

	// オブジェクト構造体にスポット構造体をリンク
	spotObjects.LinkSpots(spots)

	// エリアオブジェクト全てがピンポイントのスポットに紐づく場合
	if len(areaObjects.GetObjects()) == 0 {
		return &userId, spotObjects, nil, nil
	}

	return &userId, spotObjects, areaObjects, nil
}
