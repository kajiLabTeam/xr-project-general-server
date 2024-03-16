import express, { NextFunction, Request, Response, json } from 'express';
import morgan from 'morgan';
import { createObjectRouter } from './presentation/handler/createObjectHandler';
import { GetObjectBySpotIdRouter } from './presentation/handler/getObjectBySpotIdHandler';
import { GetObjectCollectionBySpotIdRouter } from './presentation/handler/getObjectCollectionBySpotIdsHandler';
import { DomainError } from './domain/error/domainError';
import { InfrastructureError } from './infrastructure/error/infrastructureError';

const PORT = 3000;

const app = express();

app.use(morgan('dev'));
app.use(json());

app.use(createObjectRouter);
app.use(GetObjectBySpotIdRouter);
app.use(GetObjectCollectionBySpotIdRouter);

app.listen(PORT, () => {
  console.log(`Reversi application started: http://localhost:${PORT}`);
});

app.use(errorHandler);

function errorHandler(
  err: any,
  _req: Request,
  res: Response,
  _next: NextFunction,
) {
  if (err instanceof DomainError) {
    res.status(400).send({ type: err.type, message: err.message });
    return;
  }

  if (err instanceof InfrastructureError) {
    res.status(500).send({ type: err.type, message: err.message });
    return;
  }

  res.status(500).send({ message: 'Unexpected error' });
}
