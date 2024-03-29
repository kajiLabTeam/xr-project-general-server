package services

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
)

type CreateObjectService struct {
	objectRepo repository_impl.ObjectRepositoryImpl
	spotRepo   repository_impl.SpotRepositoryImpl
}

func NewCreateObjectService(
	objectRepo repository_impl.ObjectRepositoryImpl,
	spotRepo repository_impl.SpotRepositoryImpl,
) *CreateObjectService {
	return &CreateObjectService{
		objectRepo: objectRepo,
		spotRepo:   spotRepo,
	}
}

func (cos *CreateObjectService) Run(
	userId string,
	spot *spot_models_domain.Spot,
	object *object_models_domain.Object,
	application *application_models_domain.Application,
) (*object_models_domain.Object, error) {
	// スポットをDBに登録
	spot, err := cos.spotRepo.Save(spot, application)
	if err != nil {
		return nil, err
	}

	// 登録したスポットのIDを取得
	spotId := spot.GetId()

	// オブジェクトをDBに登録
	object, err = cos.objectRepo.Save(
		spotId,
		userId,
		object,
		application,
	)
	if err != nil {
		return nil, err
	}

	// オブジェクトとスポットを紐付け
	object.LinkSpot(spot)

	return object, nil
}
