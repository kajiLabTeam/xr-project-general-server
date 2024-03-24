package repository

import (
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/domain/repository_impl"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway"
	user_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/user"
)

var ug = gateway.UserGateway{}

type UserRepository struct{}

func NewUserRepository() repository_impl.UserRepositoryImpl {
	return &UserRepository{}
}

func (ur *UserRepository) Save(
	u *user_models_domain.User,
	a *application_models_domain.Application,
) (*user_models_domain.User, error) {
	createUserRequest := user_record.SaveRequest{
		Name:       u.GetName(),
		Email:      u.GetMail(),
		Gender:     u.GetGender(),
		Age:        u.GetAge(),
		Height:     u.GetHeight(),
		Weight:     u.GetWeight(),
		Occupation: u.GetOccupation(),
		Address:    u.GetAddress(),
	}

	createSpotResponse, err := ug.Save(
		&createUserRequest,
		a,
	)
	if err != nil {
		return nil, err
	}

	resUser, err := user_models_domain.NewUser(
		&createSpotResponse.Id,
		createSpotResponse.Name,
		createSpotResponse.Email,
		createSpotResponse.Gender,
		createSpotResponse.Age,
		createSpotResponse.Height,
		createSpotResponse.Weight,
		createSpotResponse.Occupation,
		createSpotResponse.Address,
	)
	if err != nil {
		return nil, err
	}

	return resUser, nil
}
