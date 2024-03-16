package spot_models_domain

import "github.com/kajiLabTeam/xr-project-relay-server/utils"

type SpotId struct {
	value string
}

func NewSpotId(
	value *string,
) (*SpotId, error) {
	if value == nil {
		ulid, err := utils.GenerateUlid()
		if err != nil {
			return nil, err
		}
		return &SpotId{
			value: ulid,
		}, nil
	}

	return &SpotId{
		value: *value,
	}, nil
}

func (s *SpotId) GetValue() string {
	return s.value
}
