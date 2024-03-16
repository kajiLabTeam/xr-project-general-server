import { Pool } from 'pg';
import { S3Client } from '@aws-sdk/client-s3';
import { MinioEnv, PostgresEnv } from '../config/env';

export class DBConnection {
  static async connect(): Promise<Pool> {
    const postgresEnv = new PostgresEnv();

    const client = new Pool({
      user: postgresEnv.getUserOfPrivateValue(),
      host: postgresEnv.getHostOfPrivateValue(),
      database: postgresEnv.getDatabaseOfPrivateValue(),
      password: postgresEnv.getPasswordOfPrivateValue(),
      port: parseInt(postgresEnv.getPortOfPrivateValue()!),
    });

    return client.connect().then(() => client);
  }
}

export class MinioConnection {
  static async connect(): Promise<S3Client> {
    const minioEnv = new MinioEnv();

    return new S3Client({
      endpoint: minioEnv.getEndpointOfPrivateValue(),
      region: minioEnv.getRegionOfPrivateValue(),
      credentials: {
        accessKeyId: minioEnv.getAccessKeyOfPrivateValue(),
        secretAccessKey: minioEnv.getSecretKeyOfPrivateValue(),
      },
      forcePathStyle: true,
    });
  }
}
