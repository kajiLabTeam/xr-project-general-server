import { Pool } from 'pg';

import { ObjectBrowsingLogGateway } from '../gateway/objectBrowsingLogGateway';
import { ObjectBrowsingLogAggregate } from '../../domain/model/objectBrowsingLog/aggregate';
import { ObjectBrowsingLogRepositoryImpl } from '../../domain/repository_impl/objectBrowsingLogIdRepositoryImpl';
import { InfrastructureError } from '../error/infrastructureError';

const objectBrowsingLogGateway = new ObjectBrowsingLogGateway();

export class ObjectBrowsingLogRepository
  implements ObjectBrowsingLogRepositoryImpl
{
  async save(
    conn: Pool,
    objectBrowsingLog: ObjectBrowsingLogAggregate,
  ): Promise<void> {
    const objectBrowsingLogId = objectBrowsingLog
      .getIdOfPrivateValue()
      .getIdOfPrivateValue()
      .toString();
    const userId = objectBrowsingLog
      .getUserIdOfPrivateValue()
      .getIdOfPrivateValue()
      .toString();
    const objectId = objectBrowsingLog
      .getObjectIdOfPrivateValue()
      .getIdOfPrivateValue()
      .toString();

    try {
      await conn.query('BEGIN');

      await objectBrowsingLogGateway.insert(
        conn,
        objectBrowsingLogId,
        userId,
        objectId,
      );

      await conn.query('COMMIT');
    } catch (e) {
      await conn.query('ROLLBACK');

      throw new InfrastructureError('FailedToInsertObject', 'FailedToInsertObject');
    }
  }
}
