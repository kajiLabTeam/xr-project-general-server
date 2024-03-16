import express, { Request, Response, NextFunction, application } from 'express';
import { ObjectAggregate } from '../../domain/model/object/aggregate';
import { UserAggregate } from '../../domain/model/user/aggregate';
import { CreateObjectService } from '../../application/service/createObjectService';
import { ObjectRepository } from '../../infrastructure/repository/objectRepository';
import { getCredential } from '../middleware/applicationMiddleware';
import { Application } from '../../utils/globalVariable';
import { ErrorResponse } from '../error/error_presentation';

export const createObjectRouter = express.Router();

type CreateObjectRequest = {
  userId: string;
  spotId: string;
  extension: string;
};

type CreateObjectResponse = {
  id: string;
  posterId: string;
  spotId: string;
  extension: string;
  uploadUrl: string;
};

const createObjectService = new CreateObjectService(new ObjectRepository());

createObjectRouter.post(
  '/api/object/create',
  async (
    req: Request<{}, {}, CreateObjectRequest>,
    res: Response<CreateObjectResponse | ErrorResponse>,
  ) => {
    const authorization = req.headers.authorization;
    if (authorization === undefined) {
      res.status(401).send({ error: 'Unauthorized' });
      return;
    }

    const applicationId = getCredential(authorization);
    Application.id = applicationId;

    const requestBody: CreateObjectRequest = req.body;

    const userAggregate = new UserAggregate(
      UserAggregate.userIdFromStr(requestBody.userId),
    );
    const spotId = ObjectAggregate.spotIdFromStr(requestBody.spotId);
    const extension = ObjectAggregate.extensionFromStr(requestBody.extension);

    try {
      const createObjectResult = await createObjectService.run(
        userAggregate,
        spotId,
        extension,
      );

      if (createObjectResult === undefined) {
        res.status(404).send({ error: 'Internal Server Error' });
        return;
      }

      // レスポンスを送信
      const response: CreateObjectResponse = {
        id: createObjectResult
          .getIdOfPrivateValue()
          .getIdOfPrivateValue()
          .toString(),
        posterId: createObjectResult
          .getUserIdOfPrivateValue()
          .getIdOfPrivateValue()
          .getIdOfPrivateValue(),
        spotId: createObjectResult
          .getSpotIdOfPrivateValue()
          .getIdOfPrivateValue(),
        extension: createObjectResult
          .getExtensionOfPrivateValue()
          .getExtensionOfPrivateValue(),
        uploadUrl: createObjectResult
          .getSignedUrlOfPrivateValue()
          .getPreSignedUrlOfPrivateValue(),
      };

      res.status(201).json(response);
    } catch (e) {
      res.status(500).send({ error: 'Internal Server Error' });
    }
  },
);
