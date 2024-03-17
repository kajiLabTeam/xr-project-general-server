import { ObjectId } from '../object/objectId';
import { ObjectAggregate } from '../object/aggregate';
import { ObjectCollectionId } from './objectCollection';

export class ObjectCollectionAggregate {
  private _id: ObjectCollectionId;
  private _objects: ObjectAggregate[];

  constructor(_objects: ObjectAggregate[] | []) {
    this._id = new ObjectCollectionId();
    this._objects = _objects;
  }

  getIdOfPrivateValue() {
    return this._id;
  }

  getObjectsOfPrivateValue() {
    return this._objects;
  }

  addObject(object: ObjectAggregate) {
    this._objects.push(object);
  }

  removeObject(objectId: ObjectId) {
    this._objects = this._objects.filter((object) => {
      return object.getIdOfPrivateValue() !== objectId;
    });
  }
}
