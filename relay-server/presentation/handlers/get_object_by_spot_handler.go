package handlers

import (
	"mime/multipart"
	"net/http"

	"github.com/gin-gonic/gin"
	service "github.com/kajiLabTeam/xr-project-relay-server/application/services"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/repository"
	common_handler "github.com/kajiLabTeam/xr-project-relay-server/presentation/handlers/common"
	"github.com/kajiLabTeam/xr-project-relay-server/presentation/middleware"
)

type GetObjectBySpotRequest struct {
	UserId      string                `form:"userId" binding:"required"`
	Latitude    float64               `form:"latitude" binding:"required"`
	Longitude   float64               `form:"longitude" binding:"required"`
	RawDataFile *multipart.FileHeader `form:"rawDataFile" binding:"required"`
}

type GetObjectBySpotResponse struct {
	UserId      string                      `json:"userId" binding:"required"`
	SpotObjects []common_handler.ViewObject `json:"spotObjects" binding:"required"`
	AreaObjects []common_handler.ViewObject `json:"areaObjects" binding:"required"`
}

func GetObjectBySpotHandler(r *gin.Engine) {
	r.POST("api/objects/search/spot", middleware.AuthApplicationMiddleware(), func(c *gin.Context) {
		var req GetObjectBySpotRequest

		viewObjectCollectionFactory := common_handler.ViewObjectCollectionFactory{}
		applicationFactory := application_models_domain.ApplicationFactory{}
		getObjectBySpotService := service.NewGetObjectBySpotService(
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
		if err := c.Bind(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// INFO : 認証サーバーにユーザー認証をリクエスト
		// ユーザIDをパスらメータにして認証サーバーにリクエストするべきだった
		err = middleware.AuthUserMiddleware(header, req.UserId)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Unauthorized"})
			return
		}

		// ファイルを []byte に変換
		rawDataFile, err := middleware.GetBytesFromMultiPartFile(req.RawDataFile)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// サービスを実行
		resUserId, resSpotObjectCollection, resAreaObjectCollection, err := getObjectBySpotService.Run(
			req.UserId,
			req.Latitude,
			req.Longitude,
			rawDataFile,
			application,
		)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if resSpotObjectCollection == nil && resAreaObjectCollection == nil {
			res := GetObjectBySpotResponse{
				UserId:      "",
				SpotObjects: []common_handler.ViewObject{},
				AreaObjects: []common_handler.ViewObject{},
			}
			c.JSON(http.StatusNotFound, res)
			return
		}

		// レスポンスを生成
		res := GetObjectBySpotResponse{
			UserId: *resUserId,
			SpotObjects: viewObjectCollectionFactory.FromViewObjectCollection(
				resSpotObjectCollection,
			),
			AreaObjects: viewObjectCollectionFactory.FromViewObjectCollection(
				resAreaObjectCollection,
			),
		}

		// レスポンスを返却
		c.JSON(http.StatusOK, res)
	})
}
