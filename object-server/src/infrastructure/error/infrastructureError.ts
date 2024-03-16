type InfrastructureErrorType =
  | 'FailedToInsertObject'
  | 'FailedToPublishUploadPresignedUrl'
  | 'FailedToPublishViewPresignedUrl';

export class InfrastructureError extends Error {
  constructor(
    private _type: InfrastructureErrorType,
    message: string,
  ) {
    super(message);
  }

  get type() {
    return this._type;
  }
}
