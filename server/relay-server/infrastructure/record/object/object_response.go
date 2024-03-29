package object_record

import (
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
)

type ObjectResponse struct {
	Id        string `json:"id"  binding:"required"`
	PosterId  string `json:"posterId"  binding:"required"`
	SpotId    string `json:"spotId"  binding:"required"`
	Extension string `json:"extension"  binding:"required"`
	UploadUrl string `json:"viewUrl,omitempty"  binding:"required"`
}

type FindForSpotIdResponse struct {
	Id        string `json:"id"  binding:"required"`
	PosterId  string `json:"posterId"  binding:"required"`
	SpotId    string `json:"spotId"  binding:"required"`
	Extension string `json:"extension"  binding:"required"`
	ViewUrl   string `json:"viewUrl"  binding:"required,url"`
}

type SaveResponse struct {
	Id        string `json:"id"  binding:"required"`
	PosterId  string `json:"posterId"  binding:"required"`
	SpotId    string `json:"spotId"  binding:"required"`
	Extension string `json:"extension"  binding:"required"`
	UploadUrl string `json:"uploadUrl"  binding:"required,url"`
}

type FindForObjectBySpotIAndRawDataFiledResponse struct {
	Objects []*FindForSpotIdResponse `json:"objects"  binding:"required"`
}

type FindForObjectBySpotIAndRawDataFiledResponseFactory struct{}

func (f *FindForObjectBySpotIAndRawDataFiledResponseFactory) ToDomainObject(
	findForObjectBySpotIAndRawDataFiledResponse *FindForObjectBySpotIAndRawDataFiledResponse,
) (*object_collection_models_domain.ObjectCollection, error) {
	var objects []object_models_domain.Object
	for _, object := range findForObjectBySpotIAndRawDataFiledResponse.Objects {
		_object, err := object_models_domain.NewObject(
			&object.Id,
			&object.PosterId,
			object.Extension,
			&object.SpotId,
			nil,
			&object.ViewUrl,
		)
		if err != nil {
			return nil, err
		}

		objects = append(objects, *_object)
	}

	return object_collection_models_domain.NewObjectCollection(objects), nil
}
