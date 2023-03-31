# セキュリティニュースまとめ君
ChatGPTのAPIを用いて、セキュリティニュースをまとめるスクリプトおよびWebUIです。

## 使い方
Linux上で以下を実施する
* `git clone https://github.com/Sh1n0g1/security_news_matomerukun.git`
* `cd security_news_matomerukun.git`
* API Keyを[OpenAI社](https://platform.openai.com/account/api-keys)から入手する。
* `scripts/openai_key.py`にOpenAI社のAPI Keyを入力する
```python
openai_key="changeme"
```
* Dockerとして動かす
`docker build .`
