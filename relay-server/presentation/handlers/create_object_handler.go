package handlers

import (
	"mime/multipart"
	"net/http"

	"github.com/gin-gonic/gin"
	service "github.com/kajiLabTeam/xr-project-relay-server/application/services"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
	"github.com/kajiLabTeam/xr-project-relay-server/infrastructure/repository"
	"github.com/kajiLabTeam/xr-project-relay-server/presentation/middleware"
)

type CreateObjectRequest struct {
	UserId       string                `form:"userId" binding:"required"`
	Extension    string                `form:"extension" binding:"required"`
	SpotName     string                `form:"spotName" binding:"required"`
	Floor        int                   `form:"floor" binding:"required"`
	LocationType string                `form:"locationType" binding:"required"`
	Latitude     float64               `form:"latitude" binding:"required"`
	Longitude    float64               `form:"longitude" binding:"required"`
	RawDataFile  *multipart.FileHeader `form:"rawDataFile" binding:"required"`
}

type PostCreateObjectResponse struct {
	ObjectId  string `json:"objectId" binding:"required"`
	PosterId  string `json:"posterId" binding:"required"`
	Extension string `json:"extension"`
	Spot      struct {
		Id           string  `json:"id" binding:"required"`
		Name         string  `json:"name"`
		LocationType string  `json:"locationType"`
		Floor        int     `json:"floor"`
		Latitude     float64 `json:"latitude"`
		Longitude    float64 `json:"longitude"`
	} `json:"spot"`
	UploadUrl string `json:"uploadUrl" binding:"required,url"`
}

func CreateObjectHandler(r *gin.Engine) {
	r.POST("api/objects/upload", middleware.AuthApplicationMiddleware(), func(c *gin.Context) {
		var req CreateObjectRequest

		spotFactory := spot_models_domain.SpotFactory{}
		applicationFactory := application_models_domain.ApplicationFactory{}

		createObjectService := service.NewCreateObjectService(
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

		spot, err := spotFactory.Create(
			req.SpotName,
			req.Floor,
			req.LocationType,
			req.Latitude,
			req.Longitude,
			rawDataFile,
		)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		object, err := object_models_domain.NewObject(nil, nil, req.Extension, nil, nil, nil)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// サービスを実行
		resObject, err := createObjectService.Run(req.UserId, spot, object, application)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// レスポンスを生成
		res := PostCreateObjectResponse{
			ObjectId:  resObject.GetId(),
			PosterId:  resObject.GetPosterId(),
			Extension: resObject.GetExtension(),
			Spot: struct {
				Id           string  `json:"id" binding:"required"`
				Name         string  `json:"name"`
				LocationType string  `json:"locationType"`
				Floor        int     `json:"floor"`
				Latitude     float64 `json:"latitude"`
				Longitude    float64 `json:"longitude"`
			}{
				Id:           resObject.GetSpot().GetId(),
				Name:         resObject.GetSpot().GetName(),
				LocationType: resObject.GetSpot().GetLocationType(),
				Floor:        resObject.GetSpot().GetFloor(),
				Latitude:     resObject.GetSpot().GetCoordinate().GetLatitude(),
				Longitude:    resObject.GetSpot().GetCoordinate().GetLongitude(),
			},
			UploadUrl: resObject.GetPreSignedUrl(),
		}

		// レスポンスを返却
		c.JSON(http.StatusCreated, res)
	})
}
