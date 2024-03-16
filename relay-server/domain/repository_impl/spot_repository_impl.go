package repository_impl

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
)

type SpotRepositoryImpl interface {
	FindForIdsAndRawDataFile(
		spotIds []string,
		rawDataFile []byte,
		a *application_models_domain.Application,
	) (*spot_models_domain.Spot, error)

	FindForCoordinateAndRadius(
		radius int,
		lat float64,
		long float64,
		a *application_models_domain.Application,
	) (*spot_models_domain.SpotCollection, error)

	Save(
		spot *spot_models_domain.Spot,
		a *application_models_domain.Application,
	) (*spot_models_domain.Spot, error)
}
