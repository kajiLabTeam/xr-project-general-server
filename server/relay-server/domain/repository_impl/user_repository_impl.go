package repository_impl

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
)

type UserRepositoryImpl interface {
	Save(
		u *user_models_domain.User,
		a *application_models_domain.Application,
	) (*user_models_domain.User, error)
}
