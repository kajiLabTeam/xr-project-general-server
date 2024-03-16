import { Pool } from 'pg';
import { SpotId } from '../../domain/model/object/spotId';
import { ObjectCollectionAggregate } from '../../domain/model/objectCollection/aggregate';
import { S3Client } from '@aws-sdk/client-s3';

export interface ObjectCollectionRepositoryImpl {
  findByIds(
    s3: S3Client,
    conn: Pool,
    spotIds: SpotId[],
  ): Promise<ObjectCollectionAggregate | undefined>;
}
