# セキュリティニュースまとめ君
ChatGPTのAPIを用いて、セキュリティニュースを要約するプログラムです。
* DockerベースのWebアプリとスクリプトです。
* 
デフォルトはBleeping Computerのニュース記事のみを取得しています。

## 使い方
Linux上で以下を実施します。
* `git clone https://github.com/Sh1n0g1/security_news_matomerukun.git`
* `cd security_news_matomerukun.git`
* API Keyを[OpenAI社](https://platform.openai.com/account/api-keys)から入手します。
* `scripts/openai_key.py`にOpenAI社のAPI Keyを入力します。
```python
openai_key="changeme"
```
* Dockerとして動かします。
`docker build .`
完了するのに5分くらいかかります。

## カスタマイズ
