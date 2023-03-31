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
1. `cd security_news_matomerukun`
1. API Keyを[OpenAI社](https://platform.openai.com/account/api-keys)から入手します。
1. `scripts/openai_key.py`内にOpenAI社のAPI Keyを入力します。内
  `openai_key="changeme"`
1. 以下のコマンドでDocker Imageを作成します。  
`docker build . -t security_news`  
完了するのに10分くらいかかります。
1. コンテナを実行します。  
`docker run -p 80:80 security_news` 

## カスタマイズ
`script/security_news_watcher.py`の以下の部分がカスタマイズできます。
```python
# Customizable parameter
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
INTERVAL=60000 # 1 hour
rss_urls = ['https://www.bleepingcomputer.com/feed/']
# If you want to add category, you need to update the
# contents of "prompt_categorize.txt" and add 
# "prompt_<category>.txt".
categories=["incident", "vulnerability", "other"]
```
ニュース記事を取得する際の