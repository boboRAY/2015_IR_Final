# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient

client = MongoClient()
db = client.ptt_article


def get_one_article(url):
    print url
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')

    time_tag = soup.find('span', class_="article-meta-tag", text='時間')
    time = time_tag.next_sibling.get_text()

    title_tag = soup.find('span', class_="article-meta-tag", text='標題')
    title = title_tag.next_sibling.get_text()

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


urls = ['https://www.ptt.cc/bbs/NBA/M.1445998037.A.AC7.html',
        'https://www.ptt.cc/bbs/NBA/M.1446256235.A.7E3.html',
        'https://www.ptt.cc/bbs/NBA/M.1446332899.A.173.html',
        'https://www.ptt.cc/bbs/NBA/M.1446520331.A.68E.html',
        'https://www.ptt.cc/bbs/NBA/M.1446692454.A.E98.html',
        'https://www.ptt.cc/bbs/NBA/M.1446865268.A.225.html',
        'https://www.ptt.cc/bbs/NBA/M.1446949883.A.6BE.html',
        'https://www.ptt.cc/bbs/NBA/M.1447124688.A.CA8.html',
        'https://www.ptt.cc/bbs/NBA/M.1447288633.A.5D3.html',
        'https://www.ptt.cc/bbs/NBA/M.1447374611.A.2CE.html',
        'https://www.ptt.cc/bbs/NBA/M.1447556404.A.32E.html',
        'https://www.ptt.cc/bbs/NBA/M.1447815624.A.309.html',
        'https://www.ptt.cc/bbs/NBA/M.1447988461.A.CF6.html',
        'https://www.ptt.cc/bbs/NBA/M.1448074891.A.2A1.html',
        'https://www.ptt.cc/bbs/NBA/M.1448238606.A.BB5.html',
        'https://www.ptt.cc/bbs/NBA/M.1448420431.A.887.html',
        'https://www.ptt.cc/bbs/NBA/M.1448676010.A.CE8.html',
        'https://www.ptt.cc/bbs/NBA/M.1448766044.A.068.html',
        'https://www.ptt.cc/bbs/NBA/M.1448933403.A.CA1.html',
        'https://www.ptt.cc/bbs/NBA/M.1449351746.A.366.html',
        'https://www.ptt.cc/bbs/NBA/M.1449441032.A.3D4.html',
        'https://www.ptt.cc/bbs/NBA/M.1449617422.A.877.html',
        'https://www.ptt.cc/bbs/NBA/M.1449878413.A.A34.html',
        'https://www.ptt.cc/bbs/NBA/M.1449968433.A.F98.html',
        'https://www.ptt.cc/bbs/NBA/M.1450321231.A.5AE.html',
        'https://www.ptt.cc/bbs/NBA/M.1450494012.A.18B.html',
        'https://www.ptt.cc/bbs/NBA/M.1450926005.A.B5F.html',
        'https://www.ptt.cc/bbs/NBA/M.1451079004.A.A97.html',
        'https://www.ptt.cc/bbs/NBA/M.1451358011.A.1BC.html',
        'https://www.ptt.cc/bbs/NBA/M.1451523656.A.938.html',
        'https://www.ptt.cc/bbs/NBA/M.1451606763.A.969.html']

for url in urls:
    get_one_article(url)
