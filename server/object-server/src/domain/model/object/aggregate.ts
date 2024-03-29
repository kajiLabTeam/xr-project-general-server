import { SpotId } from './spotId';
import { ObjectId } from './objectId';
import { Extension } from './extension';
import { PreSignedUrl } from './preSignedUrl';
import { UserAggregate } from '../user/aggregate';

export class ObjectAggregate {
  private _id: ObjectId;
  private _extension: Extension;
  private _userId: UserAggregate;
  private _spotId: SpotId;
  private _preSignedUrl: PreSignedUrl;

  // TODO: 署名付きURLの値の持ち方を考える
  constructor(
    _extension: Extension,
    _userId: UserAggregate,
    _spotId: SpotId,
    _id: ObjectId = new ObjectId(),
    _preSignedUrl: PreSignedUrl = new PreSignedUrl(),
  ) {
    this._id = _id;
    this._extension = _extension;
    this._userId = _userId;
    this._spotId = _spotId;
    this._preSignedUrl = _preSignedUrl;
  }

  getIdOfPrivateValue() {
    return this._id;
  }

  getExtensionOfPrivateValue() {
    return this._extension;
  }

  getUserIdOfPrivateValue() {
    return this._userId;
  }

  getSpotIdOfPrivateValue() {
    return this._spotId;
  }

  getSignedUrlOfPrivateValue() {
    return this._preSignedUrl;
  }

  static idFromStr(id: string): ObjectId {
    return new ObjectId(id);
  }

  static extensionFromStr(extension: string) {
    return new Extension(extension);
  }

  static spotIdFromStr(id: string): SpotId {
    return new SpotId(id);
  }

  static spotIdsFromStr(ids: string[]): SpotId[] {
    return ids.map((id) => this.spotIdFromStr(id));
  }

  static preSignedUrlFromStr(url: string): PreSignedUrl {
    return new PreSignedUrl(url);
  }
}
