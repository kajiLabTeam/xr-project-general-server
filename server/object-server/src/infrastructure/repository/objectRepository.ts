import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { ObjectRepositoryImpl } from '../../domain/repository_impl/objectRepositoryImpl';
import { SpotId } from '../../domain/model/object/spotId';
import { Pool } from 'pg';
import { S3Client } from '@aws-sdk/client-s3';
import { ObjectGateway } from '../gateway/objectGateway';
import { UserAggregate } from '../../domain/model/user/aggregate';
import { PreSignedUrlGateway } from '../gateway/preSignedUrlGateway';
import { InfrastructureError } from '../error/infrastructureError';
import { ApplicationAggregate } from '../../domain/model/applicaation/aggregate';
import application from 'express';

const objectGateway = new ObjectGateway();
const preSignedUrlGateway = new PreSignedUrlGateway();

export class ObjectRepository implements ObjectRepositoryImpl {
  async findById(
    s3: S3Client,
    conn: Pool,
    spotId: SpotId,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined> {
    try {
      const objectRecord = await objectGateway.findById(
        conn,
        spotId.getIdOfPrivateValue(),
      );
      if (!objectRecord) {
        return undefined;
      }

      const objectRecordId = objectRecord.getIdOfPrivateValue();
      const objectRecordExtension = objectRecord.getExtensionOfPrivateValue();
      const objectRecordUserId = objectRecord.getUserIdOfPrivateValue();
      const objectRecordSpotId = objectRecord.getSpotIdOfPrivateValue();

      const fileName = `${objectRecordId}.${objectRecordExtension}`;

      const objectViewUrlRecord =
        await preSignedUrlGateway.publishViewPresignedUrl(
          s3,
          fileName,
          application.getApplicationIdOfPrivateValue(),
        );

      if (!objectViewUrlRecord) {
        return undefined;
      }

      return new ObjectAggregate(
        ObjectAggregate.extensionFromStr(objectRecordExtension),
        new UserAggregate(UserAggregate.userIdFromStr(objectRecordUserId)),
        ObjectAggregate.spotIdFromStr(objectRecordSpotId),
        ObjectAggregate.idFromStr(objectRecordId),
        ObjectAggregate.preSignedUrlFromStr(
          objectViewUrlRecord.getUrlOfPrivateValue(),
        ),
      );
    } catch (e) {
      throw new InfrastructureError(
        'FailedToPublishViewPresignedUrl',
        'FailedToPublishViewPresignedUrl',
      );
    }
  }

  async save(
    s3: S3Client,
    conn: Pool,
    object: ObjectAggregate,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined> {
    const objectId = object.getIdOfPrivateValue().getIdOfPrivateValue();
    const extension = object
      .getExtensionOfPrivateValue()
      .getExtensionOfPrivateValue();
    const userId = object
      .getUserIdOfPrivateValue()
      .getIdOfPrivateValue()
      .getIdOfPrivateValue();
    const spotId = object.getSpotIdOfPrivateValue().getIdOfPrivateValue();

    try {
      await conn.query('BEGIN');

      const objectRecord = await objectGateway.insert(
        conn,
        objectId,
        extension,
        userId,
        spotId,
      );
      if (!objectRecord) {
        return undefined;
      }

      const objectRecordId = objectRecord.getIdOfPrivateValue();
      const objectRecordExtension = objectRecord.getExtensionOfPrivateValue();
      const objectRecordUserId = objectRecord.getUserIdOfPrivateValue();
      const objectRecordSpotId = objectRecord.getSpotIdOfPrivateValue();

      const fileName = `${objectRecordId}.${objectRecordExtension}`;

      const objectUploadUrlRecord =
        await preSignedUrlGateway.publishUploadPresignedUrl(
          s3,
          fileName,
          application.getApplicationIdOfPrivateValue(),
        );

      await conn.query('COMMIT');

      return new ObjectAggregate(
        ObjectAggregate.extensionFromStr(objectRecordExtension),
        new UserAggregate(UserAggregate.userIdFromStr(objectRecordUserId)),
        ObjectAggregate.spotIdFromStr(objectRecordSpotId),
        ObjectAggregate.idFromStr(objectId),
        ObjectAggregate.preSignedUrlFromStr(
          objectUploadUrlRecord.getUrlOfPrivateValue(),
        ),
      );
    } catch (e) {
      await conn.query('ROLLBACK');

      throw new InfrastructureError(
        'FailedToInsertObject',
        'FailedToInsertObject',
      );
    }
  }
}
