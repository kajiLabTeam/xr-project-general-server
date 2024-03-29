package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/kajiLabTeam/xr-project-relay-server/application/services"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/repository"
	"github.com/kajiLabTeam/xr-project-relay-server/presentation/middleware"
)

type CreateUserRequest struct {
	Name       string  `json:"name"`
	Email      string  `json:"email"`
	Gender     string  `json:"gender"`
	Age        int     `json:"age"`
	Height     float64 `json:"height"`
	Weight     float64 `json:"weight"`
	Occupation string  `json:"occupation"`
	Address    string  `json:"address"`
}

type CreateUserResponse struct {
	Id         string  `json:"id"`
	Name       string  `json:"name"`
	Email      string  `json:"email"`
	Gender     string  `json:"gender"`
	Age        int     `json:"age"`
	Height     float64 `json:"height"`
	Weight     float64 `json:"weight"`
	Occupation string  `json:"occupation"`
	Address    string  `json:"address"`
}

func CreateUserHandler(r *gin.Engine) {
	r.POST("api/user/create", middleware.AuthApplicationMiddleware(), func(c *gin.Context) {
		var req CreateUserRequest

		applicationFactory := application_models_domain.ApplicationFactory{}
		createUserService := services.NewCreateUserService(
			repository.NewUserRepository(),
		)

		header := c.GetHeader("Authorization")
		application, err := applicationFactory.Create(header)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// リクエストのバリデーション
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		user, err := user_models_domain.NewUser(
			nil,
			req.Name,
			req.Email,
			req.Gender,
			req.Age,
			req.Height,
			req.Weight,
			req.Occupation,
			req.Address,
		)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}

		resUser, err := createUserService.Run(user, application)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		}

		res := CreateUserResponse{
			Id:         resUser.GetId(),
			Name:       resUser.GetName(),
			Email:      resUser.GetMail(),
			Gender:     resUser.GetGender(),
			Age:        resUser.GetAge(),
			Height:     resUser.GetHeight(),
			Weight:     resUser.GetWeight(),
			Occupation: resUser.GetOccupation(),
			Address:    resUser.GetAddress(),
		}

		// レスポンスを返却
		c.JSON(http.StatusCreated, res)
	})
}
