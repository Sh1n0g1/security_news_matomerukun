import os
import sys
import time
import json
import glob
import openai
import hashlib
import datetime
import html2text
import feedparser
from matomerukun_config import * 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

ARTICLES_DIR = '../articles/'
openai.api_key = openai_key

def is_article_exists(article_hash):
  files=glob.glob(ARTICLES_DIR + '/*_' + article_hash + '.json')
  if files:
    return True
  else:
    return False

def get_links_from_rss(rss_urls):
  links=[]
  for rss_url in rss_urls:
    try:
      d = feedparser.parse(rss_url)
    except Exception as e:
      exception_type, _, exc_tb = sys.exc_info()
      file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      return {
        "result": False,
        "error": f"{e} <{exception_type}> {file_name}:{exc_tb.tb_lineno}"
      }
    for entry in d.entries:
      if "published_parsed" in entry:
        pub_date=datetime.datetime.fromtimestamp(time.mktime(entry["published_parsed"]))
      else:
        pub_date=datetime.datetime.today().strftime('%Y%m%d %H%M%S')
      links.append({"title":entry.title,"link":entry.link, "pub_date": pub_date})
  return {"result": True, "links": links}

def get_web_text(url):
  options=webdriver.chrome.options.Options()
  options.add_argument(f'user-agent={USER_AGENT}')
  options.add_argument('--no-sandbox')
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--headless')
  options.add_argument('--disable-logging')
  options.add_argument('--log-level=3')
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  capabilities = options.to_capabilities()
  capabilities['acceptInsecureCerts'] = True
  chrome=webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
  try:
    chrome.get(url)
    html=chrome.page_source
    h=html2text.HTML2Text()
    h.ignore_links=True
    h.ignore_images=True
    text=h.handle(html)
    return {"result": True, "text": text}
  except Exception as e:
      exception_type, _, exc_tb = sys.exc_info()
      file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      return {"result": False, "error": f"{e} <{exception_type}> {file_name}:{exc_tb.tb_lineno}"}

def query_chatgpt_categorize(article):
  with open("prompt_categorize.txt") as f:
    order=f.read()
  try:
    result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": order,
        },{
          "role": "user",
          "content": article
        },
      ],
      max_tokens=512
    )
  except Exception as e:
    exception_type, _, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return {
      "result": False,
      "error": f"{e} <{exception_type}> {file_name}:{exc_tb.tb_lineno}"
    }
  return {
    "result": True,
    "category_result":result
  }

def query_chatgpt_summarize(article, category='other'):
  with open(f"prompt_{category}.txt") as f:
    order=f.read()
  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": order,
        },{
          "role": "user",
          "content": article
        },
      ],
      max_tokens=1024
    )
  except Exception as e:
    exception_type, _, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return {
      "result": False,
      "error": f"{e} <{exception_type}> {file_name}:{exc_tb.tb_lineno}"
    }
  return {
    "result": True,
    "response": response
  }

def sha256(text):
  return hashlib.sha256(text.encode('utf-8')).hexdigest()

def save_article(filename, article, title, category_result, category, url, pub_date, summary_results):
  with open(filename, 'w') as f:
    json.dump({
      "article":article,
      "datetime": str(pub_date),
      "title":title,
      "text_size":len(article),
      "category_result": category_result,
      "category":category,
      "url":url,
      "summary_results":summary_results
    },f)


if __name__ == "__main__":
  #Change current directory to script dir
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  run_eternally=True
  if(len(sys.argv) > 1):
    if sys.argv[1]=="oneshot":
      run_eternally=False

  print("[*] Security News Watcher")
  while True:
    print("[+] Getting RSS...")
    links=get_links_from_rss(rss_urls)
    if not links["result"]:
      print(f"[!] {links['error']}" )
      time.sleep(INTERVAL)
    for l in links:
      title=l['title']
      url=l['link']
      pub_date=l['pub_date']
      print(f"[*] Date: {str(pub_date)} Title:{title}")
      article_hash=sha256(url)
      if is_article_exists(article_hash):
        print(f"[-] Already Exists")
        continue
      file_time=pub_date.replace(":","").replace("-","")
      filename=ARTICLES_DIR + file_time + '_' + sha256(url) + '.json'
      print("[+] Getting Text...")
      text=get_web_text(url)
      if not text['result']:
        print(f"[!] Error: {text['error']}")
        filename= filename + "_error.json"
        save_article(filename, "", title, "Getting Text", "error", url, datetime.datetime.now(), [{"result": False, "error": text['error']}])
        continue
      else:
        article=text['text']
      print(f"[*] Text Size:{len(article)}")
      print("[+] Categorizing...")
      chatgpt_category_result = query_chatgpt_categorize(article)
      if not chatgpt_category_result['result']:
        category_result=chatgpt_category_result['error']
      else:
        category_result=chatgpt_category_result["category_result"].choices[0].message.content

      print(f"[*] Category:{category_result}")
      summary_results=[]
      category="other"
      for c in categories:
        if c in category_result.lower():
          category=c
          print("[+] Summarizing...")
          summary_results.append(query_chatgpt_summarize(article, c))
      #If any category does not match
      if not summary_results:
        print("[+] Summarizing...")
        summary_results.append(query_chatgpt_summarize(article))
      #Saving Result
      print("[+] Saving...")
      save_article(filename, article, title, category_result, category, url, pub_date, summary_results)
    if not run_eternally:
      break
    time.sleep(INTERVAL)
