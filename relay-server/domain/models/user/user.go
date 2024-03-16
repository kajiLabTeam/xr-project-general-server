package user_models_domain

import (
	"fmt"
)

type User struct {
	id UserId
}

func NewUser(id string) (*User, error) {
	spotId, err := NewUserId(&id)
	if err != nil {
		return nil, fmt.Errorf("failed to create user: %w", err)
	}
	return &User{id: *spotId}, nil
}

func (u *User) GetId() string {
	return u.id.GetValue()
}
