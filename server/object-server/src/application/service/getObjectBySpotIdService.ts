import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { SpotId } from '../../domain/model/object/spotId';
import { ObjectRepositoryImpl } from '../../domain/repository_impl/objectRepositoryImpl';
import { DBConnection, MinioConnection } from '../../infrastructure/connection';
import { UserId } from '../../domain/model/user/userId';
import { ObjectBrowsingLogRepositoryImpl } from '../../domain/repository_impl/objectBrowsingLogIdRepositoryImpl';
import { ObjectBrowsingLogAggregate } from '../../domain/model/objectBrowsingLog/aggregate';
import { ApplicationAggregate } from '../../domain/model/applicaation/aggregate';

export class GetObjectBySpotIdService {
  constructor(
    private _objectRepository: ObjectRepositoryImpl,
    private _objectBrowsingLogRepository: ObjectBrowsingLogRepositoryImpl,
  ) {}

  async run(
    userId: UserId,
    spotId: SpotId,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined> {
    // MinioとDBに接続する
    const conn = DBConnection.connect();
    const s3 = await MinioConnection.connect();

    // オブジェクトを取得する
    const objectRepositoryResult = await this._objectRepository.findById(
      s3,
      conn,
      spotId,
      application,
    );
    if (!objectRepositoryResult) {
      s3.destroy();
      return undefined;
    }

    // ログに残す
    const posterIdResult = objectRepositoryResult
      .getUserIdOfPrivateValue()
      .getIdOfPrivateValue();
    const objectIdResult = objectRepositoryResult.getIdOfPrivateValue();
    const objectBrowsingLog = new ObjectBrowsingLogAggregate(
      posterIdResult,
      objectIdResult,
    );
    await this._objectBrowsingLogRepository.save(conn, objectBrowsingLog);

    s3.destroy();

    return objectRepositoryResult;
  }
}
