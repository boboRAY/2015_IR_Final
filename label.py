# -*- coding: UTF-8 -*-
from pymongo import MongoClient

client = MongoClient()
db = client.ptt_article
trains = db.push_train.find()


def save_label(train, label):
    train_set = db.push_train
    new_train = {'_id': train['_id'],
                 'push': train['push'],
                 'label': label}
    train_set.update({'_id': new_train['_id']}, new_train, True)


for train in trains:
    print '\n'
    if train['label']:
        continue
    for p in train['push']:
        print p
    print '\n'
    new_label = raw_input('class is : ')
    save_label(train, new_label)
