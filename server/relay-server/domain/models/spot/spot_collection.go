package spot_models_domain

type SpotCollection struct {
	spots []Spot
}

func NewSpotCollection(spots []Spot) *SpotCollection {
	return &SpotCollection{
		spots: spots,
	}
}

func (sc *SpotCollection) GetSpots() []Spot {
	return sc.spots
}

func (sc *SpotCollection) GetSpotIds() []string {
	var spotIds []string
	for _, spot := range sc.spots {
		spotIds = append(spotIds, spot.GetId())
	}
	return spotIds
}
