# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import jieba
import numpy
import jieba
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB


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
        pushes = train['push']
        a = ''
        for push in pushes:
            a += ' '
            a += push
        train_words.append(a)
        train_label.append(label)
    return train_words, train_label


train_words, train_labels = input_data()
jieba.set_dictionary('chinese_dict.txt')
comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)
v = HashingVectorizer(tokenizer=comma_tokenizer, n_features=5000, non_negative=True)
train_data = v.fit_transform(train_words)
clf = MultinomialNB(alpha=0.01)
clf.fit(train_data, numpy.asarray(train_labels))
