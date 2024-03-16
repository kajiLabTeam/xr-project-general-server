package common_handler

import object_collection_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object_collection"

type Spot struct {
	Id           string  `json:"id"`
	Name         string  `json:"name" binding:"required"`
	Floor        int     `json:"floor" binding:"required"`
	LocationType string  `json:"locationType" binding:"required"`
	Latitude     float64 `json:"latitude" binding:"required"`
	Longitude    float64 `json:"longitude" binding:"required"`
}

type ViewObject struct {
	Id       string `json:"id"`
	PosterId string `json:"posterId"`
	Spot     Spot   `json:"spot"`
	ViewUrl  string `json:"viewUrl" binding:"required,url"`
}

type ViewObjectCollectionFactory struct{}

func (vocf *ViewObjectCollectionFactory) FromViewObjectCollection(
	objectCollection *object_collection_models_domain.ObjectCollection,
) []ViewObject {
	var viewObjects []ViewObject
	for _, object := range objectCollection.GetObjects() {
		viewObject := ViewObject{
			Id:       object.GetId(),
			PosterId: object.GetPosterId(),
			Spot: Spot{
				Id:           object.GetSpot().GetId(),
				Name:         object.GetSpot().GetName(),
				Floor:        object.GetSpot().GetFloor(),
				LocationType: object.GetSpot().GetLocationType(),
				Latitude:     object.GetSpot().GetCoordinate().GetLatitude(),
				Longitude:    object.GetSpot().GetCoordinate().GetLongitude(),
			},
			ViewUrl: object.GetPreSignedUrl(),
		}
		viewObjects = append(viewObjects, viewObject)
	}

	return viewObjects
}
