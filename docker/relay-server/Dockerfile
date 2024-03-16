# goバージョン
FROM golang:1.22.0-alpine
# アップデートとgitのインストール
RUN apk add --update &&  apk add git
# appディレクトリの作成
RUN mkdir /relay-server
# ワーキングディレクトリの設定
WORKDIR /relay-server
# ホストのファイルをコンテナの作業ディレクトリに移行
ADD . /relay-server

CMD ["go", "run", "main.go"]