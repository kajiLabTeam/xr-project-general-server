import { UserId } from './userId';

export class UserAggregate {
  private _id: UserId;

  constructor(_id: UserId = new UserId()) {
    this._id = _id;
  }

  getIdOfPrivateValue(): UserId {
    return this._id;
  }

  static userIdFromStr(id: string): UserId {
    return new UserId(id);
  }
}
