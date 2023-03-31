# セキュリティニュースまとめ君
ChatGPTのAPIを用いて、セキュリティニュースを要約するプログラムです。
* DockerベースのWebアプリとスクリプトです。
* デフォルトは[Bleeping Computer](https://www.bleepingcomputer.com/)のニュース記事のみを取得しています。

## システム要件
* Docker
* インターネットに接続できる

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
Pythonスクリプトが実行されます。1記事1分くらいの速さで取得・分類・要約が行われます。  
1. ブラウザで`http://ホストのIPアドレス/`にアクセスすると要約された記事が読めます。


## カスタマイズ
以下の項目がロジックを変更することなく、簡単にカスタマイズ可能です。

### スクリプト内
`script/security_news_watcher.py`の以下の部分がカスタマイズできます。
```python
# Customizable parameter
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
INTERVAL=3600 # 1 hour
rss_urls = ['https://www.bleepingcomputer.com/feed/']
categories=["incident", "vulnerability", "other"]
```
* `USER_AGENT`:ニュース記事を取得する際のUserAgent
* `INTERVAL`:RSSをチェックする間隔
* `rss_urls`:RSSのURL
* `categories`:カテゴリ
  * カテゴリを追加する場合、`prompt_categorize.txt`を更新し、`prompt_<category>.txt`を作成する必要があります。

### ChatGPTに対するプロンプト
`script/prompt_*.txt`となっているテキストファイルはChatGPTに送る命令の内容です。
* `prompt_categorize.txt`:記事の分類
* `prompt_incident.txt`:インシデントの記事のサマリ
* `prompt_vulnerability.txt`:脆弱性の記事のサマリ
* `prompt_other.txt`:その他の記事の記事のサマリ

### Webサイト
* `html/index.php`内の`$ARTICLES_PER_PAGE=10;`
* 1ページ当たりに表示する記事の数

## トラブルシューティング
### 動作中のコンテナのシェルを起動させる
* `docker ps`で動作しているコンテナの`NAMES`を確認する
* `docker exec -it <コンテナのNAME> /bin/bash`
