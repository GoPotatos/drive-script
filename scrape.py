import os
import requests
from lxml import html
import cloudscraper
import praw
import sys
import json
import pickle

ID=""
SECRET=""
NAME=""
PASS=""
SUBREDDIT_NAME="test"
USERAGENT="The Random User Agent"
PICKLE_PATH="cookies"
#url="https://www.vitalsource.com/en-ca/products/myers-39-psychology-for-the-ap-course-david-g-myers-v9781319121600"
url=sys.argv[1]
proxy = 'http://localhost:8080'
'''os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy'''

def normalize(text):
	stripped=text.strip()
	index=stripped.index(":")+1
	normalied_text=stripped[index:].strip()
	return normalied_text
	
	


reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    password=PASS,
    user_agent=USERAGENT,
    username=NAME,
)
browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
reddit.validate_on_submit=True


#sys.exit()
session=requests.session()

if(os.path.isfile(PICKLE_PATH)):
	with open(PICKLE_PATH,"rb") as file:
		session.cookies.update(pickle.load(file))
		file.close()
scraper = cloudscraper.create_scraper(sess=session,browser=browser)
r=scraper.get(url)

with open(PICKLE_PATH,"wb") as file:
		pickle.dump(scraper.cookies,file)
		file.close()
#r=requests.get(url)
doc=html.fromstring(r.content)
title=doc.xpath("/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div/div[2]/h1/text()")[0].strip()
author=normalize(doc.xpath("/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div/div[2]/p/text()")[0])
print_isbn=normalize(doc.xpath("/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div/div[2]/ul/li[2]/h2/text()")[0])
etext_isbn=normalize(doc.xpath("/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div/div[2]/ul/li[3]/h2/text()")[0])
edition=normalize(doc.xpath("/html/body/div[2]/main/div[3]/div/div[2]/div[1]/div/div[2]/ul/li[4]/text()")[0])

print(title,author,print_isbn,etext_isbn,edition)

#script=doc.xpath("/html/head/script[contains(@type,'application/ld+json')]/text()")[2]

#print(script)

post_title=title+" book";
selftext="Title: "+title+"\n\n"+"Author: "+author+"\n\n"+"Print ISBN: " + print_isbn + "\n\n"+"eText ISBN: "+etext_isbn+"\n\n"+"Edition: "+edition+"\n\n"
post=reddit.subreddit(SUBREDDIT_NAME).submit(title=post_title,selftext=selftext)
print(reddit.submission(post).url)