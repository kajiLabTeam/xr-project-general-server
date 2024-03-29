package services

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
)

type CreateUserService struct {
	userRepo repository_impl.UserRepositoryImpl
}

func NewCreateUserService(
	userRepo repository_impl.UserRepositoryImpl,
) *CreateUserService {
	return &CreateUserService{
		userRepo: userRepo,
	}
}

func (cus *CreateUserService) Run(
	u *user_models_domain.User,
	a *application_models_domain.Application,
) (
	*user_models_domain.User,
	error,
) {
	// userのインスタンスをDBに保存
	resUser, err := cus.userRepo.Save(u, a)
	if err != nil {
		return nil, err
	}

	return resUser, nil
}
