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

def get_link():
  links=[]
  for rss_url in rss_urls:
    d = feedparser.parse(rss_url)
    for entry in d.entries:
      links.append({"title":entry.title,"link":entry.link})
  return links

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

if __name__ == "__main__":
  #Change current directory to script dir
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  run_eternally=True
  if(len(sys.argv) > 1):
    if sys.argv[1]=="oneshot":
      run_eternally=False

  print("[*] Security News Watcher")
  while True:
    print("[+] Getting CSS...")
    links=get_link()
    for l in links:
      title=l['title']
      url=l['link']
      print(f"[*] Title:{title}")
      article_hash=sha256(url)
      if is_article_exists(article_hash):
        print(f"[-] Already Exists")
        continue
      current_time=datetime.datetime.today().strftime('%Y%m%d %H%M%S')
      filename=ARTICLES_DIR + current_time + '_' + sha256(url) + '.json'
      print("[+] Getting Text...")
      text=get_web_text(url)
      if not text['result']:
        print(f"[!] Error: {text['error']}")
        continue
      article=text['text']
      print(f"[*] Text Size:{len(article)}")
      print("[+] Categorizing...")
      chatgpt_category_result = query_chatgpt_categorize(article)
      if not chatgpt_category_result['result']:
        category_result=chatgpt_category_result['error']
      else:
        category_result=chatgpt_category_result["category_result"].choices[0].message.content

      print(f"[*] Category:{category_result}")
      results=[]
      category="other"
      for c in categories:
        if c in category_result.lower():
          category=c
          print("[+] Summarizing...")
          results.append(query_chatgpt_summarize(article, c))
      #If any category does not match
      if not results:
        print("[+] Summarizing...")
        results.append(query_chatgpt_summarize(article))
      #Saving Result
      print("[+] Saving...")
      with open(filename, 'w') as f:
        json.dump({
          "article":article,
          "datetime": str(datetime.datetime.now()),
          "title":title,
          "text_size":len(article),
          "category_result": category_result,
          "category":category,
          "url":url,
          "results":results
        },f)
    if not run_eternally:
      break
    time.sleep(INTERVAL)
