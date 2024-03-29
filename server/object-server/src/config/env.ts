import { config } from 'dotenv';

config();
export class PostgresEnv {
  private _host: string;
  private _database: string;
  private _user: string;
  private _password: string;
  private _port: string;

  constructor() {
    this._host = process.env.POSTGRES_HOST!;
    this._database = process.env.POSTGRES_DB!;
    this._user = process.env.POSTGRES_USER!;
    this._password = process.env.POSTGRES_PASSWORD!;
    this._port = process.env.POSTGRES_PORT!;
  }

  getHostOfPrivateValue() {
    return this._host;
  }

  getDatabaseOfPrivateValue() {
    return this._database;
  }

  getUserOfPrivateValue() {
    return this._user;
  }

  getPasswordOfPrivateValue() {
    return this._password;
  }

  getPortOfPrivateValue() {
    return this._port;
  }
}

export class MinioEnv {
  private _serviceName: string = 's3';
  private _region: string;
  private _endpoint: string;
  private _accessKey: string;
  private _secretKey: string;

  constructor() {
    this._region = process.env.MINIO_REGION!;
    this._endpoint = process.env.MINIO_ENDPOINT!;
    this._accessKey = process.env.MINIO_ACCESS_KEY!;
    this._secretKey = process.env.MINIO_SECRET_KEY!;
  }

  getServiceNameOfPrivateValue() {
    return this._serviceName;
  }

  getRegionOfPrivateValue() {
    return this._region;
  }

  getEndpointOfPrivateValue() {
    return this._endpoint;
  }

  getAccessKeyOfPrivateValue() {
    return this._accessKey;
  }

  getSecretKeyOfPrivateValue() {
    return this._secretKey;
  }
}
