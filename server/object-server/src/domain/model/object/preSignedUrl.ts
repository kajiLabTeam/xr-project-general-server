import * as url from 'url';
import { DomainError } from '../../error/domainError';

export class PreSignedUrl {
  private _preSignedUrl: string;

  constructor(preSignedUrl: string = '') {
    if (preSignedUrl !== '' && !this.isValidUrl(preSignedUrl)) {
      throw new DomainError('InvalidPreSignedUrl', 'Invalid pre-signed URL');
    }
    this._preSignedUrl = preSignedUrl;
  }

  getPreSignedUrlOfPrivateValue(): string {
    return this._preSignedUrl;
  }

  private isValidUrl(testUrl: string): boolean {
    try {
      const parsedUrl = new url.URL(testUrl);
      return true;
    } catch (error) {
      return false;
    }
  }
}
