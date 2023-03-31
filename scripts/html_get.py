
import os
import sys
import json
import requests
import html2text
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
DEBUG=False
FILE_DIR='scripts/htmls/'

def is_url(url):
  prepared_request=requests.models.PreparedRequest()
  try:
    prepared_request.prepare_url(url, None)
    return True
  except:
    return False

def get_html(url):
  if not is_url(url):
    return {"result": False, "error": "URL is broken."}
  options=webdriver.chrome.options.Options()
  options.add_argument(f'user-agent={USER_AGENT}')
  options.add_argument('--no-sandbox')
  options.add_argument('--ignore-certificate-errors')
  if not DEBUG:
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
    return {"result": True, "html": html}
  except Exception as e:
      exception_type, _, exc_tb = sys.exc_info()
      file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      return {"result": False, "error": f"{e} <{exception_type}> {file_name}:{exc_tb.tb_lineno}"}

def get_text_from_html(html):
  h=html2text.HTML2Text()
  h.ignore_links=True
  h.ignore_images=True
  text=h.handle(html)
  print(text)
  return text

if __name__ == '__main__':
  if(len(sys.argv) < 3):
    print("Usage: python html_get.py <url> <file>")
    exit()
  
  url=sys.argv[1]
  filename=sys.argv[2]
  html=get_html(url)
  if html['result']:
    html['html']=get_text_from_html(html['html'])
  else:
    print(json.dumps(html))
    exit(100)
  
  with open(FILE_DIR + filename,'w') as f:
    json.dump(html,f)
  #print(json.dumps(html, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))