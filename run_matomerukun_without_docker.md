# まとめる君をUbuntu上で直接で動かす方法（非Docker）
⚠️工事中⚠️ 詳しい方はDockerfileの中身を見ればわかると思います。以下の手順はまだちゃんと動作確認が取れておりません。
## セットアップ
* Ubuntuを用意します。推奨バージョン:`22.04`
* 以下のコマンドをroot権限のあるユーザで実行します。
```bash
apt-get update
apt-get install apache2 -y
apt-get install php libapache2-mod-php -y 
service apache2 start
rm /var/www/html/index.html

apt-get install python3 -y
apt-get install python3-pip -y
pip3 install openai
pip3 install feedparser
pip3 install html2text

apt-get install wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install ./google-chrome-stable_current_amd64.deb -y 
pip3 install selenium webdriver-manager

git clone https://github.com/Sh1n0g1/security_news_matomerukun.git

cd security_news_matomerukun
cp ./scripts/ /var/www/
cp ./html/index.php /var/www/html/
mkdir /var/www/articles/
chown www-data:www-data /var/www/articles/
```

* `/var/www/scripts/openai_key.py`にOpenAI社のAPIキーを入力する

## 実行
```
python3 /var/www/scripts/security_news_watcher.py oneshot
```
* oneshotパラメータを実行することにより、Pythonが無限に実行されません。

cronなどで`python3 /var/www/scripts/security_news_watcher.py oneshot`をしかければ、記事のまとめが定期に行われます。
例)  
```cron
30 * * * * (python3 /var/www/scripts/security_news_matomerukun.py | logger)
```