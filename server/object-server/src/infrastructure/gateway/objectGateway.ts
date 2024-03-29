import { Pool } from 'pg';
import { ObjectRecord } from '../record/objectRecord';
import { InfrastructureError } from '../error/infrastructureError';

export class ObjectGateway {
  async findById(
    conn: Pool,
    spotId: string,
  ): Promise<ObjectRecord | undefined> {
    try {
      const objectSelectResult = await conn.query(
        'SELECT * FROM objects WHERE spot_id = $1',
        [spotId],
      );

      if (objectSelectResult.rows && objectSelectResult.rows.length > 0) {
        const object = objectSelectResult.rows[0];
        return new ObjectRecord(
          object.id,
          object.extension,
          object.user_id,
          object.spot_id,
          object.created_at,
        );
      }

      return undefined;
    } catch (e) {
      throw e;
    }
  }

  async findByIds(
    conn: Pool,
    spotIds: string[],
  ): Promise<ObjectRecord[] | undefined> {
    const objectSelectResult = await conn.query(
      'SELECT * FROM objects WHERE spot_id = ANY($1)',
      [spotIds],
    );

    if (objectSelectResult.rows && objectSelectResult.rows.length > 0) {
      return objectSelectResult.rows.map((object: any) => {
        return new ObjectRecord(
          object.id,
          object.extension,
          object.user_id,
          object.spot_id,
          object.created_at,
        );
      });
    }

    return undefined;
  }

  async insert(
    conn: Pool,
    objectId: string,
    extension: string,
    userId: string,
    spotId: string,
  ): Promise<ObjectRecord | undefined> {
    const objectInsertResult = await conn.query(
      'INSERT INTO objects (id, extension, user_id, spot_id) VALUES ($1, $2, $3, $4) RETURNING *',
      [objectId, extension, userId, spotId],
    );

    if (objectInsertResult.rows && objectInsertResult.rows.length > 0) {
      const object = objectInsertResult.rows[0];
      return new ObjectRecord(
        object.id,
        object.extension,
        object.user_id,
        object.spot_id,
        object.created_at,
      );
    } else {
      throw new InfrastructureError(
        'FailedToInsertObject',
        'Failed to insert object',
      );
    }
  }
}
