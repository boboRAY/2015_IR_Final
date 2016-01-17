# -*- coding: UTF-8 -*-
from pymongo import MongoClient

client = MongoClient()
db = client.ptt_article

#regx = re.compile("^Live", re.IGNORECASE)
#articles = db.articles.find({"title": regx})
articles = db.articles.find()



def create_pushlist(push):
    pre_date = 0
    pushes_minute = []
    window = []
    for push in pushes:
        date = push['date']
        if not pre_date or pre_date == date:
            window.append(push)
        else:
            pushes_minute.append(window)
            window = []
            window.append(push)
        pre_date = date
    return pushes_minute


def save_label(push,label):
    train = {'label' : label,
             'push' : push}
    train_set = db.push_train
    train_set.insert_one(train)



def get_peak(pushes_minute):
    for i in range(2, len(pushes_minute)):
        pre = pushes_minute[i-2]
        mid = pushes_minute[i-1]
        nex = pushes_minute[i]
        if len(mid)>40 and len(mid) > len(pre) and len(mid) > len(nex):
            # for i in range(len(pre)/2,len(pre)):
                # s = pre[i]['content']
                # save_pushes.append(s)
                #print s
            for i in [20,35]:
                content = []
                for i in range(i-1,i+2):    
                    content.append(mid[i]['content'])
                save_label(content,0)
                # print content
            # for i in range(0,len(nex)/2):
                # s = nex[i]['content']
                # save_pushes.append(s)
                #print s


for article in articles:
    print article['title']
    pushes = article['pushes']
    pushes_minute = create_pushlist(pushes)
    get_peak(pushes_minute)
