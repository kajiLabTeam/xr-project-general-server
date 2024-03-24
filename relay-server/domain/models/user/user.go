package user_models_domain

import (
	"fmt"

	"github.com/kajiLabTeam/xr-project-relay-server/utils"
)

type User struct {
	id         UserId
	name       string
	mail       string
	gender     string
	age        int
	height     float64
	weight     float64
	occupation string
	address    string
}

func NewUser(
	id *string,
	name string,
	mail string,
	gender string,
	age int,
	height float64,
	weight float64,
	occupation string,
	address string,
) (*User, error) {
	userId, err := NewUserId(id)
	if err != nil {
		return nil, err
	}

	if len(name) > 50 {
		return nil, fmt.Errorf("name is too long")
	}

	if !utils.ValidateEmail(&mail) {
		return nil, fmt.Errorf("invalid email")
	}

	return &User{
		id:         *userId,
		name:       name,
		mail:       mail,
		gender:     gender,
		age:        age,
		height:     height,
		weight:     weight,
		occupation: occupation,
		address:    address,
	}, nil
}

func (u *User) GetId() string {
	return u.id.GetValue()
}

func (u *User) GetName() string {
	return u.name
}

func (u *User) GetMail() string {
	return u.mail
}

func (u *User) GetGender() string {
	return u.gender
}

func (u *User) GetAge() int {
	return u.age
}

func (u *User) GetHeight() float64 {
	return u.height
}

func (u *User) GetWeight() float64 {
	return u.weight
}

func (u *User) GetOccupation() string {
	return u.occupation
}

func (u *User) GetAddress() string {
	return u.address
}

