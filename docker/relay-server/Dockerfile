FROM golang:1.22.0-alpine

RUN mkdir /relay-server

WORKDIR /relay-server

COPY ./relay-server /relay-server
COPY /.env /relay-server/.env

CMD ["go", "run", "main.go"]
