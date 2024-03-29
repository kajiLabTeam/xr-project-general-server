package spot_record

import "mime/multipart"

type FindForIdsAndRawDataFileRequest struct {
	RawDataFile []byte   `json:"rawDataFile"  binding:"required"`
}

type FindForCoordinateAndRadiusRequest struct {
	Latitude  float64 `json:"latitude"  binding:"required"`
	Longitude float64 `json:"longitude"  binding:"required"`
}

type SaveRequest struct {
	Id           string                `form:"id" binding:"required"`
	Name         string                `form:"name" binding:"required"`
	Floor        int                   `form:"floor" binding:"required"`
	LocationType string                `form:"locationType" binding:"required"`
	Latitude     float64               `form:"latitude" binding:"required"`
	Longitude    float64               `form:"longitude" binding:"required"`
	RawDataFile  *multipart.FileHeader `form:"rawDataFile"`
}
