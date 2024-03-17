import { ApplicationAggregate } from '../../domain/model/applicaation/aggregate';
import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { Extension } from '../../domain/model/object/extension';
import { SpotId } from '../../domain/model/object/spotId';
import { UserAggregate } from '../../domain/model/user/aggregate';
import { ObjectRepositoryImpl } from '../../domain/repository_impl/objectRepositoryImpl';
import { DBConnection, MinioConnection } from '../../infrastructure/connection';

export class CreateObjectService {
  constructor(private _objectRepository: ObjectRepositoryImpl) {}

  async run(
    user: UserAggregate,
    spotId: SpotId,
    extension: Extension,
    application: ApplicationAggregate,
  ): Promise<ObjectAggregate | undefined> {
    // MinioとDBに接続する
    const s3 = await MinioConnection.connect();
    const conn = await DBConnection.connect();

    // オブジェクトを生成する
    const object = new ObjectAggregate(extension, user, spotId);

    // オブジェクトを保存する
    const objectRepositoryResult = await this._objectRepository.save(
      s3,
      conn,
      object,
      application,
    );
    // オブジェクトが保存できなかった場合
    if (!objectRepositoryResult) {
      return undefined;
    }

    return objectRepositoryResult;
  }
}
