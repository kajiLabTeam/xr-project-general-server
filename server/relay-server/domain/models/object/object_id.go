package object_models_domain

import "github.com/kajiLabTeam/xr-project-relay-server/utils"

type ObjectId struct {
	value string
}

func NewObjectId(
	value *string,
) (*ObjectId, error) {
	if value == nil {
		ulid, err := utils.GenerateUlid()
		if err != nil {
			return nil, err
		}
		return &ObjectId{
			value: ulid,
		}, nil
	}

	return &ObjectId{
		value: *value,
	}, nil
}

func (o *ObjectId) GetValue() string {
	return o.value
}
