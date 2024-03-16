package spot_models_domain

import "fmt"

type LocationType struct {
	value string
}

func NewLocationType(value string) (*LocationType, error) {
	if value != "indoor" && value != "outdoor" {
		return nil, fmt.Errorf("invalid locationType value")
	}

	return &LocationType{value: value}, nil
}

func (lt *LocationType) GetValue() string {
	return lt.value
}
