package spot_record

import spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"

type SpotResponse struct {
	Spots        []SpotResponse `json:"spots"  binding:"required"`
	Id           string         `json:"id"  binding:"required,uuid"`
	Name         string         `json:"name"  binding:"required"`
	Floor        int            `json:"floor"  binding:"required"`
	LocationType string         `json:"locationType"  binding:"required"`
	Latitude     float64        `json:"latitude"  binding:"required"`
	Longitude    float64        `json:"longitude"  binding:"required"`
}

type FindForIdAndRawDataFileResponse struct {
	Spots        []SpotResponse `json:"spots"  binding:"required"`
	Id           string         `json:"id"  binding:"required,uuid"`
	Name         string         `json:"name"  binding:"required"`
	Floor        int            `json:"floor"  binding:"required"`
	LocationType string         `json:"locationType"  binding:"required"`
	Latitude     float64        `json:"latitude"  binding:"required"`
	Longitude    float64        `json:"longitude"  binding:"required"`
}

type FindForIdsAndRawDataFileResponse struct {
	Spots []SpotResponse `json:"spots"  binding:"required"`
}

func (f *FindForIdsAndRawDataFileResponse) AddSpotResponse(
	spot *SpotResponse,
) {
	f.Spots = append(f.Spots, *spot)
}

type FindForCoordinateAndRadiusResponse struct {
	Spots []SpotResponse `json:"spots"  binding:"required"`
}

type SaveResponse struct {
	Id           string  `json:"id"  binding:"required,uuid"`
	Name         string  `json:"name"  binding:"required"`
	Floor        int     `json:"floor"  binding:"required"`
	LocationType string  `json:"locationType"  binding:"required"`
	Latitude     float64 `json:"latitude"  binding:"required"`
	Longitude    float64 `json:"longitude"  binding:"required"`
}

type FindForIdsAndRawDataFileResponseFactory struct{}

func (f *FindForIdsAndRawDataFileResponseFactory) ToDomainSpotCollection(
	findForCoordinateAndRadiusResponse *FindForIdsAndRawDataFileResponse,
) (*spot_models_domain.SpotCollection, error) {
	var spots []spot_models_domain.Spot
	for _, spot := range findForCoordinateAndRadiusResponse.Spots {
		_spot, err := spot_models_domain.NewSpot(
			&spot.Id,
			spot.Name,
			&spot.LocationType,
			spot.Floor,
			spot.Latitude,
			spot.Longitude,
			nil,
		)
		if err != nil {
			return nil, err
		}
		spots = append(spots, *_spot)
	}

	return spot_models_domain.NewSpotCollection(spots), nil
}

type FindForCoordinateAndRadiusResponseFactory struct{}

func (f *FindForCoordinateAndRadiusResponseFactory) ToDomainSpotCollection(
	findForCoordinateAndRadiusResponse *FindForCoordinateAndRadiusResponse,
) (*spot_models_domain.SpotCollection, error) {
	var spots []spot_models_domain.Spot
	for _, spot := range findForCoordinateAndRadiusResponse.Spots {
		_spot, err := spot_models_domain.NewSpot(
			&spot.Id,
			spot.Name,
			&spot.LocationType,
			spot.Floor,
			spot.Latitude,
			spot.Longitude,
			nil,
		)
		if err != nil {
			return nil, err
		}
		spots = append(spots, *_spot)
	}

	return spot_models_domain.NewSpotCollection(spots), nil
}
