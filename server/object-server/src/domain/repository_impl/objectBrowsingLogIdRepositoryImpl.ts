import { Pool } from 'pg';
import { ObjectBrowsingLogAggregate } from '../model/objectBrowsingLog/aggregate';

export interface ObjectBrowsingLogRepositoryImpl {
  save(
    conn: Pool,
    objectBrowsingLog: ObjectBrowsingLogAggregate,
  ): Promise<void>;
}
