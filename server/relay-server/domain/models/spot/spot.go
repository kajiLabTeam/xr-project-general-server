package spot_models_domain

type Spot struct {
	id           SpotId
	name         string
	locationType LocationType
	floor        int
	coordinate   Coordinate
	rawDataFile  *[]byte
}

func NewSpot(
	id *string,
	name string,
	locationType *string,
	floor int,
	latitude float64,
	longitude float64,
	rawDataFile *[]byte,
) (*Spot, error) {
	spotId, err := NewSpotId(id)
	if err != nil {
		return nil, err
	}

	_locationType, err := NewLocationType(*locationType)
	if err != nil {
		return nil, err
	}

	coordinate, err := NewCoordinate(latitude, longitude)
	if err != nil {
		return nil, err
	}

	return &Spot{
		id:           *spotId,
		name:         name,
		locationType: *_locationType,
		floor:        floor,
		coordinate:   *coordinate,
		rawDataFile:  rawDataFile,
	}, nil
}

func (s *Spot) GetId() string {
	return s.id.GetValue()
}

func (s *Spot) GetName() string {
	return s.name
}

func (s *Spot) GetLocationType() string {
	return s.locationType.GetValue()
}

func (s *Spot) GetFloor() int {
	return s.floor
}

func (s *Spot) GetCoordinate() *Coordinate {
	return &s.coordinate
}

func (s *Spot) GetRawDataFile() []byte {
	return *s.rawDataFile
}

type SpotFactory struct{}

func (sp *SpotFactory) Create(
	name string,
	floor int,
	locationType string,
	latitude float64,
	longitude float64,
	rawDataFile []byte,
) (*Spot, error) {
	return NewSpot(
		nil,
		name,
		&locationType,
		floor,
		latitude,
		longitude,
		&rawDataFile,
	)
}
