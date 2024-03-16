package object_models_domain

import (
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
)

type Object struct {
	id           ObjectId
	posterId     *user_models_domain.UserId
	extension    string
	spotId       *spot_models_domain.SpotId
	spot         *spot_models_domain.Spot
	preSignedUrl *PreSignedUrl
}

func NewObject(
	id *string,
	posterId *string,
	extension string,
	spotId *string,
	spot *spot_models_domain.Spot,
	preSignedUrl *string,
) (*Object, error) {
	objectId, err := NewObjectId(id)
	if err != nil {
		return nil, err
	}

	_posterId, err := user_models_domain.NewUserId(posterId)
	if err != nil {
		return nil, err
	}

	_spotId, err := spot_models_domain.NewSpotId(spotId)
	if err != nil {
		return nil, err
	}

	_preSignedUrl, err := NewPreSignedUrl(preSignedUrl)
	if err != nil {
		return nil, err
	}

	return &Object{
		id:           *objectId,
		posterId:     _posterId,
		extension:    extension,
		spotId:       _spotId,
		spot:         spot,
		preSignedUrl: _preSignedUrl,
	}, nil
}

func (o *Object) GetId() string {
	return o.id.GetValue()
}

func (o *Object) GetPosterId() string {
	return o.posterId.GetValue()
}

func (o *Object) GetExtension() string {
	return o.extension
}

func (o *Object) GetSpotId() string {
	return o.spotId.GetValue()
}

func (o *Object) GetSpot() *spot_models_domain.Spot {
	return o.spot
}

func (o *Object) GetPreSignedUrl() string {
	return o.preSignedUrl.GetValue()
}

func (o *Object) LinkSpot(spot *spot_models_domain.Spot) {
	// nil参照エラーを避けるために、既にスポットが紐付いている場合は何もしない
	if spot == nil {
		return
	}
	if o.GetSpotId() != spot.GetId() {
		return
	}

	o.spot = spot
}

type ObjectFactory struct{}

func (f *ObjectFactory) Create(
	extension string,
) (*Object, error) {
	return NewObject(nil, nil, extension, nil, nil, nil)
}
