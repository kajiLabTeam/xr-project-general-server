package object_collection_models_domain

import (
	object_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/object"
	spot_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/spot"
)

type ObjectCollection struct {
	objects []object_models_domain.Object
}

func NewObjectCollection(objects []object_models_domain.Object) *ObjectCollection {
	return &ObjectCollection{
		objects: objects,
	}
}

func (oc *ObjectCollection) GetObjects() []object_models_domain.Object {
	return oc.objects
}

func (oc *ObjectCollection) AddObject(object *object_models_domain.Object) {
	oc.objects = append(oc.objects, *object)
}

func (oc *ObjectCollection) LinkSpots(spot_collection *spot_models_domain.SpotCollection) {
	// nil参照エラーを避けるために、スポットがない場合は何もしない
	if len(spot_collection.GetSpots()) == 0 {
		return
	}
	for i, object := range oc.objects {
		for _, spot := range spot_collection.GetSpots() {
			if object.GetSpotId() == spot.GetId() {
				oc.objects[i].LinkSpot(&spot)
			}
		}
	}
}
