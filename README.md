# セキュリティニュースまとめ君
ChatGPTのAPIを用いて、セキュリティニュースを要約するプログラムです。
* DockerベースのWebアプリとスクリプトです。
* 
デフォルトはBleeping Computerのニュース記事のみを取得しています。

## システム要件
* Dockerが入っていること

## 使い方
Linux上で以下を実施します。
1. `git clone https://github.com/Sh1n0g1/security_news_matomerukun.git`
1. `cd security_news_matomerukun.git`
1. API Keyを[OpenAI社](https://platform.openai.com/account/api-keys)から入手します。
1. `scripts/openai_key.py`にOpenAI社のAPI Keyを入力します。
  ```python
  openai_key="changeme"
  ```
5. 以下のコマンドでDocker Imageを作成します。  
`docker build . -t security_news`  
完了するのに10分くらいかかります。
1. Docker Image一覧を確認し、作成されたことを確認します。  
`docker images`  
1. 以下の通り表示されます。
```
REPOSITORY             TAG       IMAGE ID       CREATED              SIZE
security_news          latest    bf528a9d8c8e   About a minute ago   1.43GB
```
1.コンテナを実行します。
`docker run `

## カスタマイズ
