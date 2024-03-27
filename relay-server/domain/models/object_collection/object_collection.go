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

func (oc *ObjectCollection) GetObjectIds() []string {
	var object_ids []string
	for _, object := range oc.objects {
		object_ids = append(object_ids, object.GetId())
	}
	return object_ids
} 

func (oc *ObjectCollection) AddObject(object *object_models_domain.Object) {
	oc.objects = append(oc.objects, *object)
}

func (oc *ObjectCollection) RemoveObjectById(object_id string) {
	for i, object := range oc.objects {
		if object.GetId() == object_id {
			oc.objects = append(oc.objects[:i], oc.objects[i+1:]...)
		}
	}
}

func (oc *ObjectCollection) RemoveObjectByIds(object_ids []string) {
	for _, object_id := range object_ids {
		oc.RemoveObjectById(object_id)
	}
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
