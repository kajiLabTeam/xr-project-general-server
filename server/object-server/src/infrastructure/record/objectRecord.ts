export class ObjectRecord {
  constructor(
    private _id: string,
    private _extension: string,
    private _userId: string,
    private _spotId: string,
    private _createdAt: Date,
  ) {}

  getIdOfPrivateValue(): string {
    return this._id;
  }

  getExtensionOfPrivateValue(): string {
    return this._extension;
  }

  getUserIdOfPrivateValue(): string {
    return this._userId;
  }

  getSpotIdOfPrivateValue(): string {
    return this._spotId;
  }

  getCreatedAtOfPrivateValue(): Date {
    return this._createdAt;
  }
}
