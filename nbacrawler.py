# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient
import re
import time
import random

client = MongoClient()
db = client.ptt_article


def get_one_article(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')

    try:
        time_tag = soup.find('span', class_="article-meta-tag", text='時間')
        time = time_tag.next_sibling.get_text()
        title_tag = soup.find('span', class_="article-meta-tag", text='標題')
        title = title_tag.next_sibling.get_text()
        print title
    except:
        print 'article error',url
        return

    rawpushes = soup.find_all('div', class_='push')
    pushes = []
    for push in rawpushes:
        p = push.find_all('span')
        if not p:
            continue
        pushdict = {'type': p[0].get_text(), 'id': p[1].get_text(), 'content': p[2].get_text()[2:], 'date': p[3].get_text()}
        pushes.append(pushdict)
    article = {'time': time, 'title': title, 'pushes': pushes}
    articles = db.articles
    articles.insert_one(article)


def get_onepage_live_url(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    blocks = soup.find_all('div', class_='r-ent')
    urls = []
    for block in blocks:
        urlblock = block.find('a', text=re.compile('Live'))
        if urlblock:
            url = 'https://www.ptt.cc/'+urlblock['href']
            urls.append(url)
    return urls


def next_page(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    nextbtn = soup.find('a', text='‹ 上頁')
    return 'https://www.ptt.cc/'+nextbtn['href']


url = 'https://www.ptt.cc/bbs/NBA/index3420.html'

for i in range(1, 2000):
    print 'page', i
    while True:
        try:
            urls = get_onepage_live_url(url)
            url = next_page(url)
            break
        except:
            time.sleep(1)
            print 'except1 ', url
            continue
    for link in urls:
        while True:
            try:
                get_one_article(link)
                break
            except urllib2.HTTPError, err:
                print 'except2 ', link
                t = random.randint(1, 5)
                time.sleep(t)
