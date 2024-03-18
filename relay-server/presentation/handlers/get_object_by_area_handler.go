package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/kajiLabTeam/xr-project-relay-server/application/services"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	user_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/user"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/repository"
	common_handler "github.com/kajiLabTeam/xr-project-relay-server/presentation/handlers/common"
	"github.com/kajiLabTeam/xr-project-relay-server/presentation/middleware"
)

type GetObjectByAreaRequest struct {
	UserId    string  `json:"userId" binding:"required"`
	Latitude  float64 `json:"latitude" binding:"required"`
	Longitude float64 `json:"longitude" binding:"required"`
}

type GetObjectByAreaResponse struct {
	UserId  string                      `json:"userId" binding:"required"`
	Objects []common_handler.ViewObject `json:"objects"`
}

func GetObjectByAreaHandler(r *gin.Engine) {
	r.POST("api/objects/search/area", middleware.AuthMiddleware(), func(c *gin.Context) {
		var req GetObjectByAreaRequest

		viewObjectCollectionFactory := common_handler.ViewObjectCollectionFactory{}
		applicationFactory := application_models_domain.ApplicationFactory{}
		getObjectByAreaService := services.NewGetObjectByAreaService(
			repository.NewObjectRepository(),
			repository.NewSpotRepository(),
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

		// クエリパラメータの取得
		area, err := strconv.Atoi(c.Query("radius"))
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		user, err := user_models_domain.NewUser(req.UserId)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// サービスを実行
		user, objectCollection, err := getObjectByAreaService.Run(
			area,
			req.Latitude,
			req.Longitude,
			user,
			application,
		)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if objectCollection == nil {
			res := GetObjectByAreaResponse{
				UserId:  user.GetId(),
				Objects: []common_handler.ViewObject{},
			}

			c.JSON(http.StatusNotFound, res)
		}

		res := GetObjectByAreaResponse{
			UserId:  user.GetId(),
			Objects: viewObjectCollectionFactory.FromViewObjectCollection(objectCollection),
		}

		c.JSON(http.StatusOK, res)
	})
}
