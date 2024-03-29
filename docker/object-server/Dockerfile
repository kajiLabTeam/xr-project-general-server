FROM node:20.5.1-alpine

WORKDIR /object-server

COPY /server/object-server /object-server
COPY /.env /object-server/.env

RUN npm install

CMD ["npm", "start"]
