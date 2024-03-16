# エリア推定サーバ

> [!IMPORTANT]
> 環境変数は[こちらから](https://kjlb.esa.io/posts/5242)確認してください

## 実行方法
### DBコンテナの立ち上げ
```bash
make up
```
### モジュールインストール
`pipenv`が入っていない場合
```bash
brew install pipenv
```

```bash
pipenv install
```

### 仮想環境にログイン
```bash
pipenv shell
```

### サーバの実行
```bash
python src/main.py
```

## その他
### DBコンテナに入りたいとき
```bash
make db
```
