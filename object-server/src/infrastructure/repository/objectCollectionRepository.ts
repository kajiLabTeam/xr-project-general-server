import { Pool } from 'pg';
import { SpotId } from '../../domain/model/object/spotId';
import { ObjectCollectionAggregate } from '../../domain/model/objectCollection/aggregate';
import { UserId } from '../../domain/model/user/userId';
import { ObjectCollectionRepositoryImpl } from '../../domain/repository_impl/objectCollectionRepositoryImpl';
import { ObjectGateway } from '../gateway/objectGateway';
import { PreSignedUrlGateway } from '../gateway/preSignedUrlGateway';
import { S3Client } from '@aws-sdk/client-s3';
import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { UserAggregate } from '../../domain/model/user/aggregate';
import { InfrastructureError } from '../error/infrastructureError';
import application from 'express';
import { ApplicationAggregate } from '../../domain/model/applicaation/aggregate';

const objectGateway = new ObjectGateway();
const preSignedUrlGateway = new PreSignedUrlGateway();

export class ObjectCollectionRepository
  implements ObjectCollectionRepositoryImpl
{
  async findByIds(
    s3: S3Client,
    conn: Pool,
    spotIds: SpotId[],
    application: ApplicationAggregate,
  ): Promise<ObjectCollectionAggregate | undefined> {
    const objectCollectionRecord = await objectGateway.findByIds(
      conn,
      spotIds.map((spotId) => spotId.getIdOfPrivateValue()),
    );
    if (!objectCollectionRecord) {
      return undefined;
    }

    const objectCollectionAggregate = new ObjectCollectionAggregate([]);

    for (const objectRecord of objectCollectionRecord) {
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
        continue;
      } else {
        objectCollectionAggregate.addObject(
          new ObjectAggregate(
            ObjectAggregate.extensionFromStr(objectRecordExtension),
            new UserAggregate(UserAggregate.userIdFromStr(objectRecordUserId)),
            ObjectAggregate.spotIdFromStr(objectRecordSpotId),
            ObjectAggregate.idFromStr(objectRecordId),
            ObjectAggregate.preSignedUrlFromStr(
              objectViewUrlRecord.getUrlOfPrivateValue(),
            ),
          ),
        );
      }
    }

    return objectCollectionAggregate;
  }
}
