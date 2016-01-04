# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

client = MongoClient()
db = client.ptt_article

articles = {}
article = db.articles.find_one({'_id': ObjectId('5686910d3e103d28540d60c0')})
# cursor = db.articles.find()

pushes = article['pushes']
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
'''
f = open('peak.txt', 'w')
for i in range(2, len(pushes_minute)):
    pre = pushes_minute[i-2]
    mid = pushes_minute[i-1]
    nex = pushes_minute[i]
    if len(mid) > len(pre) and len(mid) > len(nex):
        f.write(mid[0]['date']+'\n')
        for push in mid:
            f.write(push['content'].encode('utf-8')+'\n')
            print push['content'], push['date']
        f.write('\n')
        print '\n'
f.close()
'''
pushes_len = []
for pushes in pushes_minute:
    pushes_len.append(len(pushes)+1)
# evenly sampled time at 200ms intervals
t = np.arange(len(pushes_minute))
# red dashes, blue squares and green triangles
plt.plot(t, pushes_len, marker='o')
plt.show()
