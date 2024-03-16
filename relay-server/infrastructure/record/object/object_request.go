package object_record

type FindForSpotIdRequest struct {
	UserId string `json:"userId"  binding:"required"`
	SpotId string `json:"spotId"  binding:"required"`
}

type FindForSpotIdsRequest struct {
	UserId  string   `json:"userId"  binding:"required"`
	SpotIds []string `json:"spotIds"  binding:"required"`
}

type SaveRequest struct {
	UserId    string `json:"userId"  binding:"required"`
	SpotId    string `json:"spotId"  binding:"required"`
	Extension string `json:"extension"  binding:"required"`
}
