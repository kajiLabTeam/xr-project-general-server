import { Pool } from 'pg';

export class ObjectBrowsingLogGateway {
  async insert(
    conn: Pool,
    objectBrowsingLogId: string,
    userId: string,
    objectId: string,
  ): Promise<void> {
    try {
      await conn.query('BEGIN');

      await conn.query(
        'INSERT INTO object_browsing_logs (id, user_id, object_id) VALUES ($1, $2, $3)',
        [objectBrowsingLogId, userId, objectId],
      );

      await conn.query('COMMIT');
    } catch (e) {
      await conn.query('ROLLBACK');

      throw e;
    }

    return;
  }
}
