FROM ubuntu:22.04
LABEL maintainer "Sh1n0g1"
#To skip the timezone input
ENV DEBIAN_FRONTEND=noninteractive

#Install Apache + PHP
RUN apt update && \
    apt install apache2 -y && \
    apt install php libapache2-mod-php -y

#Install Python and its library
RUN apt install python3 -y &&\
apt install python3-pip -y && \
pip3 install openai &&\
pip3 install feedparser &&\
pip3 install html2text

#Install Chrome & Selenium
RUN apt-get install wget &&\
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
apt install ./google-chrome-stable_current_amd64.deb -y &&\
pip3 install selenium webdriver-manager 

#Prepare Files & Dirs
RUN mkdir /var/www/scripts/ &&\
mkdir /var/www/articles/ &&\
chown www-data:www-data /var/www/articles/
COPY scripts/ /var/www/scripts/
COPY html /var/www/html

EXPOSE 80

CMD [python3 /var/www/scripts/security_news_watcher.py]