openai_key="changeme"

# Customizable parameter
## The user agent used to access to the news site.
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

# The Interval to check the RSS Feed
INTERVAL=3600 # 1 hour

# RSS Feed URL
rss_urls = ['https://www.bleepingcomputer.com/feed/']

# Category
## If you want to add category, you need to update the
## contents of "prompt_categorize.txt" and add 
## "prompt_<category>.txt".

categories=["incident", "vulnerability", "other"]