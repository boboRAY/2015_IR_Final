# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import jieba
import numpy
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
from collections import Counter

client = MongoClient()
db = client.ptt_article
trains = db.push_train.find()



def input_data():
    train_words = []
    train_label = []
    for train in trains:
        label = train['label']
        if label not in ['2', '3', '4', '5', '6']:
            continue
        pushes = train['push']
        a = ''
        for push in pushes:
            a += ' '
            a += push
        train_words.append(a)
        train_label.append(label)
    return train_words, train_label


def vectorize(data):
    jieba.set_dictionary('chinese_dict.txt')
    comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)
    v = HashingVectorizer(tokenizer=comma_tokenizer, n_features= 400, non_negative=True)
    adata = v.fit_transform(data)
    return adata


def train():
    train_words, train_labels = input_data()
    train_data = vectorize(train_words)
    clf = MultinomialNB(alpha=0.01)
    clf.fit(train_data, numpy.asarray(train_labels))
    return clf


test_article = db.articles.find_one({'_id': ObjectId("568bd0c377f9021458259cbe")})


# jieba.set_dictionary('dict.txt.big')
# jieba.load_userdict('chinese_dict.txt')
jieba.set_dictionary('chinese_dict.txt')


# set pushes into time frame
pushes = test_article['pushes']
pre_date = 0
pushes_minute = []
window = []
for push in pushes:
    date = datetime.strptime(push['date'], ' %m/%d %H:%M ')
    if not pre_date or pre_date == date:
        window.append(push)
    else:
        pushes_minute.append(window)
        window = []
        window.append(push)
    pre_date = date

# plot
pushes_len = []
for pushes in pushes_minute:
    pushes_len.append(len(pushes)+1)
t = np.arange(len(pushes_minute))
plt.plot(t, pushes_len, marker='o')
plt.show()

# find peak and classify
clf = train()
test_data = {}
for i in range(2, len(pushes_minute)):
    pre = pushes_minute[i-2]
    mid = pushes_minute[i-1]
    nex = pushes_minute[i]
    if len(mid) > len(pre) and len(mid) > len(nex) and len(mid) > 20:
        pushes = []
        for push in mid:
            content = push['content']
            pushes.append(content)
            print content
        test_data = vectorize(pushes)
        pred = clf.predict(test_data)
        common = [ite for ite, it in Counter(pred).most_common(1)]
        label =  common[0]
        if label == '2':
            label = '兩分'
        elif label == '3':
            label = '三分'
        elif label == '4':
            label = '放槍'
        elif label == '5':
            label = '失誤'
        elif label == '6':
            label = '犯規'
        print '=================================='
        print '事件：' + label
        raw_input('pause')
