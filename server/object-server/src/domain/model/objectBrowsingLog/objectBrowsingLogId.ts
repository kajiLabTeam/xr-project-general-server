import { ulid } from 'ulid';

export class ObjectBrowsingLogId {
  protected _id: string;

  constructor(id = ulid()) {
    this._id = id;
  }

  getIdOfPrivateValue(): string {
    return this._id;
  }
}
