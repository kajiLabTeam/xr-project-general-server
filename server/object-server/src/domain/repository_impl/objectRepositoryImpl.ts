import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { SpotId } from '../../domain/model/object/spotId';
import { Pool } from 'pg';
import { S3Client } from '@aws-sdk/client-s3';
import { ApplicationAggregate } from '../model/applicaation/aggregate';

export interface ObjectRepositoryImpl {
  findById(
    s3: S3Client,
    conn: Pool,
    spotId: SpotId,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined>;

  save(
    s3: S3Client,
    conn: Pool,
    object: ObjectAggregate,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined>;
}
