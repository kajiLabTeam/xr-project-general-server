package repository

import (
	"sync"

	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway"
	spot_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/spot"
)

var sg = gateway.SpotGateway{}

type SpotRepository struct{}

func NewSpotRepository() repository_impl.SpotRepositoryImpl {
	return &SpotRepository{}
}

func (sr *SpotRepository) FindForIdsAndRawDataFile(
	spotIds []string,
	rawDataFile []byte,
	a *application_models_domain.Application,
) (*spot_models_domain.SpotCollection, error) {
	findForIdsAndRawDataFileResponseFactory := spot_record.FindForIdsAndRawDataFileResponseFactory{}
	findForIdsAndRawDataFileRes := spot_record.FindForIdsAndRawDataFileResponse{}

	var wg sync.WaitGroup
	for _, id := range spotIds {
		wg.Add(1)

		go func(id string) error {
			defer wg.Done()

			findForIdAndRawDataFileRes, err := sg.FindForIdAndRawDataFile(
				id,
				rawDataFile,
				a,
			)
			if err != nil {
				return err
			}
			if findForIdAndRawDataFileRes != nil {
				findForIdsAndRawDataFileRes.AddSpotResponse(&findForIdAndRawDataFileRes.Spots[0])
			}

			return nil
		}(id)

		wg.Wait()
	}

	if len(findForIdsAndRawDataFileRes.Spots) == 0 {
		return nil, nil
	}

	resSpotCollection, err := findForIdsAndRawDataFileResponseFactory.ToDomainSpotCollection(
		&findForIdsAndRawDataFileRes,
	)
	if err != nil {
		return nil, err
	}
	if resSpotCollection == nil {
		return nil, nil
	}

	return resSpotCollection, nil
}

func (sr *SpotRepository) FindForCoordinateAndRadius(
	radius int,
	latitude float64,
	longitude float64,
	application *application_models_domain.Application,
) (*spot_models_domain.SpotCollection, error) {
	findForObjectBySpotIAndRawDataFiledResFactory := spot_record.FindForCoordinateAndRadiusResponseFactory{}
	findForCoordinateAndRadiusReq := spot_record.FindForCoordinateAndRadiusRequest{
		Latitude:  latitude,
		Longitude: longitude,
	}

	findForCoordinateAndRadiusRes, err := sg.FindForCoordinateAndRadius(
		radius,
		&findForCoordinateAndRadiusReq,
		application,
	)
	if err != nil {
		return nil, err
	}
	if findForCoordinateAndRadiusRes == nil {
		return nil, nil
	}

	resSpotCollection, err := findForObjectBySpotIAndRawDataFiledResFactory.ToDomainSpotCollection(
		findForCoordinateAndRadiusRes,
	)
	if err != nil {
		return nil, err
	}

	return resSpotCollection, nil
}

func (sr *SpotRepository) Save(
	spot *spot_models_domain.Spot,
	a *application_models_domain.Application,
) (*spot_models_domain.Spot, error) {
	createSpotRequest := spot_record.SaveRequest{
		Name:         spot.GetName(),
		LocationType: spot.GetLocationType(),
		Floor:        spot.GetFloor(),
		Latitude:     spot.GetCoordinate().GetLatitude(),
		Longitude:    spot.GetCoordinate().GetLongitude(),
	}

	createSpotResponse, err := sg.Save(
		spot.GetRawDataFile(),
		&createSpotRequest,
		a,
	)
	if err != nil {
		return nil, err
	}

	resSpot, err := spot_models_domain.NewSpot(
		&createSpotResponse.Id,
		createSpotResponse.Name,
		&createSpotResponse.LocationType,
		createSpotResponse.Floor,
		createSpotResponse.Latitude,
		createSpotResponse.Longitude,
		nil,
	)
	if err != nil {
		return nil, err
	}

	return resSpot, nil
}
