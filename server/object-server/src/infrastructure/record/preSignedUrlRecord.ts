export class UploadPresignedUrlRecord {
  constructor(private _url: string) {}

  getUrlOfPrivateValue(): string {
    return this._url;
  }
}

export class ViewPreSignedUrlRecord {
  constructor(private _url: string) {}

  getUrlOfPrivateValue(): string {
    return this._url;
  }
}
