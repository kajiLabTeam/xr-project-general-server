import express, { Request, Response } from 'express';

import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { UserAggregate } from '../../domain/model/user/aggregate';
import { GetObjectCollectionBySpotIdService } from '../../application/service/getObjectCollectionBySpotIdsService';
import { ObjectBrowsingLogRepository } from '../../infrastructure/repository/objectBrowsingLogRepository';
import { ObjectCollectionRepository } from '../../infrastructure/repository/objectCollectionRepository';
import { Application } from '../../utils/globalVariable';
import { getCredential } from '../middleware/applicationMiddleware';
import { ErrorResponse } from '../error/error_presentation';

export const GetObjectCollectionBySpotIdRouter = express.Router();

type GetObjectCollectionBySpotIdRequest = {
  userId: string;
  spotIds: string[];
};

type ObjectItem = {
  id: string;
  extension: string;
  posterId: string;
  spotId: string;
  viewUrl: string;
};

type GetObjectCollectionBySpotIdResponse = {
  objects: ObjectItem[];
};

const getObjectCollectionBySpotIdService =
  new GetObjectCollectionBySpotIdService(
    new ObjectCollectionRepository(),
    new ObjectBrowsingLogRepository(),
  );

GetObjectCollectionBySpotIdRouter.post(
  '/api/object/collection/get',
  async (
    req: Request<{}, {}, GetObjectCollectionBySpotIdRequest>,
    res: Response<GetObjectCollectionBySpotIdResponse | ErrorResponse>,
  ) => {
    const authorization = req.headers.authorization;
    if (authorization === undefined) {
      res.status(401).send({ error: 'Unauthorized' });
      return;
    }

    const applicationId = getCredential(authorization);
    Application.id = applicationId;

    const requestBody: GetObjectCollectionBySpotIdRequest = req.body;

    if (requestBody.spotIds === null || requestBody.spotIds.length === 0) {
      const response: GetObjectCollectionBySpotIdResponse = {
        objects: [],
      };

      res.status(404).json(response);
      return;
    }

    const userId = UserAggregate.userIdFromStr(requestBody.userId);
    const spotIds = ObjectAggregate.spotIdsFromStr(requestBody.spotIds);

    try {
      const getObjectCollectionBySpotIdResult =
        await getObjectCollectionBySpotIdService.run(userId, spotIds);
      if (getObjectCollectionBySpotIdResult === undefined) {
        res.status(404).json({ error: 'Object Not Found' });
        return;
      }

      // レスポンスを送信
      const response: GetObjectCollectionBySpotIdResponse = {
        objects: getObjectCollectionBySpotIdResult
          .getObjectsOfPrivateValue()
          .map((object) => {
            return {
              id: object.getIdOfPrivateValue().getIdOfPrivateValue(),
              extension: object
                .getExtensionOfPrivateValue()
                .getExtensionOfPrivateValue(),
              posterId: object
                .getUserIdOfPrivateValue()
                .getIdOfPrivateValue()
                .getIdOfPrivateValue(),
              spotId: object.getSpotIdOfPrivateValue().getIdOfPrivateValue(),
              viewUrl: object
                .getSignedUrlOfPrivateValue()
                .getPreSignedUrlOfPrivateValue(),
            };
          }),
      };

      res.json(response);
    } catch (e) {
      res.status(500).send({ error: 'Internal Server Error' });
    }
  },
);
