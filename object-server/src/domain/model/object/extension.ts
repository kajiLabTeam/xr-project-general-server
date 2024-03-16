import { DomainError } from '../../error/domainError';

export class Extension {
  private _extension: string;

  constructor(extension: string) {
    if (extension.length > 10) {
      throw new DomainError(
        'ExtensionMustBeLessThan10Characters',
        'Extension must be less than 10 characters',
      );
    }
    this._extension = extension;
  }

  getExtensionOfPrivateValue() {
    return this._extension;
  }
}
