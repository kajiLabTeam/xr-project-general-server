import { ulid } from 'ulid';

export class ObjectCollectionId {
  protected _id: string;

  constructor(id = ulid()) {
    this._id = id;
  }
}
