# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import jieba

client = MongoClient()
db = client.ptt_article

articles = {}
articles = db.articles.find_one()

articles = [articles]

jieba.load_userdict('chinese_dict.txt')


f = open('output.txt','w')

for article in articles:
    pushes = article['pushes']
    for push in pushes:
        content = push['content']
        words = jieba.cut(content)
        for word in words:
            f.write(word.encode('utf-8') + ' ')
        f.write('\n')
