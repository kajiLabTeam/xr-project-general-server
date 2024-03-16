# goバージョン
FROM golang:1.22.0-alpine
# アップデートとgitのインストール
RUN apk add --update &&  apk add git
# appディレクトリの作成
RUN mkdir /application-authentication-server
# ワーキングディレクトリの設定
WORKDIR /application-authentication-server
# ホストのファイルをコンテナの作業ディレクトリに移行
ADD . /application-authentication-server

CMD ["go", "run", "main.go"]