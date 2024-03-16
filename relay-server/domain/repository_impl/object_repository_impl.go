package repository_impl

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
)

type ObjectRepositoryImpl interface {
	FindForSpotId(
		spotId string,
		u *user_models_domain.User,
		a *application_models_domain.Application,
	) (*object_models_domain.Object, error)

	FindForSpotIds(
		spotIds []string,
		u *user_models_domain.User,
		a *application_models_domain.Application,
	) (*object_collection_models_domain.ObjectCollection, error)

	Save(
		spotId string,
		u *user_models_domain.User,
		o *object_models_domain.Object,
		a *application_models_domain.Application,
	) (*object_models_domain.Object, error)
}
