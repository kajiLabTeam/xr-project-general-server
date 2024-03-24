package repository_impl

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
)

type ObjectRepositoryImpl interface {
	FindForSpotId(
		spotId string,
		userId string,
		a *application_models_domain.Application,
	) (*object_models_domain.Object, error)

	FindForSpotIds(
		userId string,
		spotIds []string,
		a *application_models_domain.Application,
	) (*object_collection_models_domain.ObjectCollection, error)

	Save(
		spotId string,
		userId string,
		o *object_models_domain.Object,
		a *application_models_domain.Application,
	) (*object_models_domain.Object, error)
}
