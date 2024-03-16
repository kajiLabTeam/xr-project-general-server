import express, { ErrorRequestHandler, Request, Response } from 'express';

import { UserAggregate } from '../../domain/model/user/aggregate';
import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { GetObjectBySpotIdService } from '../../application/service/getObjectBySpotIdService';
import { ObjectRepository } from '../../infrastructure/repository/objectRepository';
import { ObjectBrowsingLogRepository } from '../../infrastructure/repository/objectBrowsingLogRepository';
import { getCredential } from '../middleware/applicationMiddleware';
import { Application } from '../../utils/globalVariable';
import { ErrorResponse } from '../error/error_presentation';

export const GetObjectBySpotIdRouter = express.Router();

type GetObjectBySpotIdRequest = {
  userId: string;
  spotId: string;
};

type GetObjectBySpotIdResponse = {
  id: string;
  posterId: string;
  spotId: string;
  viewUrl: string;
};

const getObjectBySpotIdService = new GetObjectBySpotIdService(
  new ObjectRepository(),
  new ObjectBrowsingLogRepository(),
);

GetObjectBySpotIdRouter.post(
  '/api/object/get',
  async (
    req: Request<{}, {}, GetObjectBySpotIdRequest>,
    res: Response<GetObjectBySpotIdResponse | ErrorResponse>,
  ) => {
    const authorization = req.headers.authorization;
    if (authorization === undefined) {
      res.status(401).send({ error: 'Unauthorized' });
      return;
    }

    const applicationId = getCredential(authorization);
    Application.id = applicationId;

    const requestBody: GetObjectBySpotIdRequest = req.body;

    try {
      const userAggregate = new UserAggregate(
        UserAggregate.userIdFromStr(requestBody.userId),
      );
      const spotId = ObjectAggregate.spotIdFromStr(requestBody.spotId);

      const getObjectBySpotIdResult = await getObjectBySpotIdService.run(
        userAggregate.getIdOfPrivateValue(),
        spotId,
      );
      if (getObjectBySpotIdResult === undefined) {
        res.status(404).send({ error: 'Spot Not Found' });
        return;
      }

      const response: GetObjectBySpotIdResponse = {
        id: getObjectBySpotIdResult.getIdOfPrivateValue().getIdOfPrivateValue(),
        posterId: getObjectBySpotIdResult
          .getUserIdOfPrivateValue()
          .getIdOfPrivateValue()
          .getIdOfPrivateValue(),
        spotId: getObjectBySpotIdResult
          .getSpotIdOfPrivateValue()
          .getIdOfPrivateValue(),
        viewUrl: getObjectBySpotIdResult
          .getSignedUrlOfPrivateValue()
          .getPreSignedUrlOfPrivateValue(),
      };
      res.json(response);
    } catch (e) {
      res.status(500).send({ error: 'Internal Server Error' });
    }
  },
);
