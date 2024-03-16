export class ObjectCollectionRecord {
  constructor(
    private _id: string,
    private _name: string,
    private _createdAt: Date,
    private _updatedAt: Date,
  ) {}

  getIdOfPrivateValue(): string {
    return this._id;
  }

  getNameOfPrivateValue(): string {
    return this._name;
  }

  getCreatedAtOfPrivateValue(): Date {
    return this._createdAt;
  }

  getUpdatedAtOfPrivateValue(): Date {
    return this._updatedAt;
  }
}
