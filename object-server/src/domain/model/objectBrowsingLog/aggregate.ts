import { ObjectId } from '../object/objectId';
import { UserId } from '../user/userId';
import { ObjectBrowsingLogId } from './objectBrowsingLogId';

export class ObjectBrowsingLogAggregate {
  private _id: ObjectBrowsingLogId;
  private _userId: UserId;
  private _objectId: ObjectId;

  constructor(
    _userId: UserId,
    _objectId: ObjectId,
    _id: ObjectBrowsingLogId = new ObjectBrowsingLogId(),
  ) {
    this._id = _id;
    this._userId = _userId;
    this._objectId = _objectId;
  }

  getIdOfPrivateValue() {
    return this._id;
  }

  getUserIdOfPrivateValue() {
    return this._userId;
  }

  getObjectIdOfPrivateValue() {
    return this._objectId;
  }
}
