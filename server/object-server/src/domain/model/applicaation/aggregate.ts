export class ApplicationAggregate {
  private _applicationId: string;
  private _secretKey: string;

  constructor(applicationId: string, secretKey: string) {
    this._applicationId = applicationId;
    this._secretKey = secretKey;
  }

  getApplicationIdOfPrivateValue() {
    return this._applicationId;
  }

  getSecretKeyOfPrivateValue() {
    return this._secretKey;
  }
}
