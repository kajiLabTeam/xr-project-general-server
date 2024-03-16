import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { SpotId } from '../../domain/model/object/spotId';
import { Pool } from 'pg';
import { S3Client } from '@aws-sdk/client-s3';

export interface ObjectRepositoryImpl {
  findById(
    s3: S3Client,
    conn: Pool,
    spotId: SpotId,
  ): Promise<ObjectAggregate | undefined>;

  save(
    s3: S3Client,
    conn: Pool,
    object: ObjectAggregate,
  ): Promise<ObjectAggregate | undefined>;
}
