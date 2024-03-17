import { ApplicationAggregate } from '../../domain/model/applicaation/aggregate';
import { SpotId } from '../../domain/model/object/spotId';
import { ObjectCollectionAggregate } from '../../domain/model/objectCollection/aggregate';
import { UserId } from '../../domain/model/user/userId';
import { ObjectBrowsingLogRepositoryImpl } from '../../domain/repository_impl/objectBrowsingLogIdRepositoryImpl';
import { ObjectCollectionRepositoryImpl } from '../../domain/repository_impl/objectCollectionRepositoryImpl';
import { DBConnection, MinioConnection } from '../../infrastructure/connection';

export class GetObjectCollectionBySpotIdService {
  constructor(
    private _objectCollectionRepository: ObjectCollectionRepositoryImpl,
    private _objectBrowsingLogRepository: ObjectBrowsingLogRepositoryImpl,
  ) {}

  async run(
    userId: UserId,
    spotIds: SpotId[],
    application: ApplicationAggregate,
  ): Promise<ObjectCollectionAggregate | undefined> {
    // MinioとDBに接続する
    const s3 = await MinioConnection.connect();
    const conn = await DBConnection.connect();

    // オブジェクト配列で取得する
    const objectCollection = await this._objectCollectionRepository.findByIds(
      s3,
      conn,
      spotIds,
      application,
    );
    if (objectCollection === undefined) {
      return undefined;
    }

    return objectCollection;
  }
}
