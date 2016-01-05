# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import re

client = MongoClient()
db = client.ptt_article

articles = {}
articles = db.articles.find()


def list2bigram(mylist):
    return [mylist[i:i+2] for i in range(0, len(mylist)-1)]


def allngram(text):
    words = {}
    for n in range(1, len(text)):
        for w in range(len(text)-(n-1)):
            word = text[w:w+n]
            if word in words:
                words[word] = words[word] + 1
            else:
                words[word] = 1
    return words


dictionary = {}
for article in articles:
    print article['title']
    for push in article['pushes']:
        content = push['content']
        for ctext in re.findall(ur'[\u4e00-\u9fff]+', content):
            words = allngram(ctext)
            for word in words:
                if word in dictionary:
                    dictionary[word] = dictionary[word] + words[word]
                else:
                    dictionary[word] = words[word]

f = open('dicitonary.txt','w')
for word, freq in sorted(dictionary.items(), key=lambda x:x[1]):
    f.write(word.encode('utf-8')+'   ')
    freq = dictionary[word]
    f.write(str(freq))
    f.write('\n')

f.close()