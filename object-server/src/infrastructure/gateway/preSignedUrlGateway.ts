import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import {
  GetObjectCommand,
  PutObjectCommand,
  S3Client,
} from '@aws-sdk/client-s3';
import {
  APPLICATION_BUCKET_NAME,
  OBJECTS_BUCKET_NAME,
  UPLOAD_URL_LIFETIME,
  VIEW_URL_LIFETIME,
} from '../../config/const';
import {
  UploadPresignedUrlRecord,
  ViewPreSignedUrlRecord,
} from '../record/preSignedUrlRecord';
import { Application } from '../../utils/globalVariable';

export class PreSignedUrlGateway {
  async publishUploadPresignedUrl(
    s3: S3Client,
    key: string,
  ): Promise<UploadPresignedUrlRecord> {
    try {
      const objectKey = `${Application.id}/${OBJECTS_BUCKET_NAME}/${key}`;
      const url = await getSignedUrl(
        s3,
        new PutObjectCommand({
          Bucket: APPLICATION_BUCKET_NAME,
          Key: objectKey,
        }) as any,
        { expiresIn: UPLOAD_URL_LIFETIME },
      );

      return new UploadPresignedUrlRecord(url);
    } catch (e) {
      throw e;
    }
  }

  async publishViewPresignedUrl(
    s3: S3Client,
    key: string,
  ): Promise<ViewPreSignedUrlRecord> {
    try {
      const objectKey = `${Application.id}/${OBJECTS_BUCKET_NAME}/${key}`;
      const url = await getSignedUrl(
        s3,
        new GetObjectCommand({
          Bucket: APPLICATION_BUCKET_NAME,
          Key: objectKey,
        }) as any,
        { expiresIn: VIEW_URL_LIFETIME },
      );

      return new ViewPreSignedUrlRecord(url);
    } catch (e) {
      throw e;
    }
  }
}
