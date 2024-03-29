FROM golang:1.22.0-alpine

WORKDIR /application-authentication-server

COPY /server/application-authentication-server /application-authentication-server
COPY /.env /application-authentication-server/.env

CMD ["go", "run", "main.go"]
