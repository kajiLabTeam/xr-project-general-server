# goバージョン
FROM node:20.5.1-alpine
# アップデートとgitのインストール
RUN apk add --update &&  apk add git
# appディレクトリの作成
RUN mkdir /object-server
# ワーキングディレクトリの設定
WORKDIR /object-server

CMD ["npm", "start"]
