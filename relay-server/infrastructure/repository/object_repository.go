package repository

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway"
	object_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/object"
)

var og = gateway.ObjectGateway{}

type ObjectRepository struct{}

func NewObjectRepository() repository_impl.ObjectRepositoryImpl {
	return &ObjectRepository{}
}

func (or *ObjectRepository) FindForSpotId(
	spotId string,
	u *user_models_domain.User,
	a *application_models_domain.Application,
) (*object_models_domain.Object, error) {
	FindForSpotIdRequest := object_record.FindForSpotIdRequest{
		UserId: u.GetId(),
		SpotId: spotId,
	}

	// ゲートウェイを介してスポットを取得
	getObjectBySpotIdRes, err := og.FindForSpotId(
		&FindForSpotIdRequest,
		a,
	)
	if err != nil {
		return nil, err
	}

	resObject, err := object_models_domain.NewObject(
		&getObjectBySpotIdRes.Id,
		&getObjectBySpotIdRes.PosterId,
		getObjectBySpotIdRes.Extension,
		&getObjectBySpotIdRes.SpotId,
		nil,
		&getObjectBySpotIdRes.ViewUrl,
	)
	if err != nil {
		return nil, err
	}

	return resObject, nil

}

func (or *ObjectRepository) FindForSpotIds(
	spotIds []string,
	u *user_models_domain.User,
	a *application_models_domain.Application,
) (*object_collection_models_domain.ObjectCollection, error) {
	findForObjectBySpotIAndRawDataFiledResFactory := object_record.FindForObjectBySpotIAndRawDataFiledResponseFactory{}
	findForSpotIdAndRawDataRequest := object_record.FindForSpotIdsRequest{
		UserId:  u.GetId(),
		SpotIds: spotIds,
	}

	// ゲートウェイを介してスポットを取得
	findForSpotIdAndRawDataRes, err := og.FindForSpotIds(
		&findForSpotIdAndRawDataRequest,
		a,
	)
	if err != nil {
		return nil, err
	}
	if findForSpotIdAndRawDataRes == nil {
		return nil, nil
	}

	resObjectCollection, err := findForObjectBySpotIAndRawDataFiledResFactory.ToDomainObject(
		findForSpotIdAndRawDataRes,
	)
	if err != nil {
		return nil, err
	}

	return resObjectCollection, nil

}

func (or *ObjectRepository) Save(
	spotId string,
	u *user_models_domain.User,
	o *object_models_domain.Object,
	a *application_models_domain.Application,
) (*object_models_domain.Object, error) {
	createObjectRequest := object_record.SaveRequest{
		UserId:    u.GetId(),
		SpotId:    spotId,
		Extension: o.GetExtension(),
	}

	// ゲートウェイを介してスポットを保存
	saveObjectRes, err := og.Save(&createObjectRequest, a)
	if err != nil {
		return nil, err
	}

	resObject, err := object_models_domain.NewObject(
		&saveObjectRes.Id,
		&saveObjectRes.PosterId,
		saveObjectRes.Extension,
		&saveObjectRes.SpotId,
		nil,
		&saveObjectRes.UploadUrl,
	)
	if err != nil {
		return nil, err
	}

	return resObject, nil
}
