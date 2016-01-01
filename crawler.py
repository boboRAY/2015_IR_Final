# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2


def get_one_article(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    time_tag = soup.find('span', class_="article-meta-tag", text='時間')
    time = time_tag.next_sibling.get_text()
    print time
    title_tag = soup.find('span', class_="article-meta-tag", text='標題')
    title = title_tag.next_sibling.get_text()
    print title
    pushes = soup.find_all('div', class_='push')
    for push in pushes:
        for line in push.find_all('span'):
            print line.get_text()

url = 'https://www.ptt.cc/bbs/NBA/M.1451606763.A.969.html'
get_one_article(url)
