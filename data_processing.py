import pandas as pd
import numpy as np
import re

train = pd.read_csv('./Train_Data.csv')
test = pd.read_csv('./Test_Data.csv')
def stop_words(x):
    try:
        x = x.strip()
    except:
        return ''
    x = re.sub('\?\?+','',x)
    x = re.sub('\{IMG:.?.?.?\}','',x)
    return x
    
    
train['text_new']= train['title']+','+train['text']
train['text_new'] = train['text_new'].apply(stop_words)
train = train[(train['title'].notnull())|(train['text'].notnull())]

final_data_set = []
for i in train[['unknownEntities','text_new']].values:
    temp = list(i[1])
    try:
        for t in re.finditer(i[0],i[1]):
            for num in range(t.span()[0],t.span()[1]):
                if num==t.span()[0]:
                    temp[num] = temp[num]+' B-ORG'
                elif num==t.span()[1]-1:
                    temp[num] = temp[num]+' E-ORG'
                else:
                    temp[num] = temp[num]+' I-ORG'
    except:
        1
    for i in range(len(temp)):
        if ("B-ORG" not in temp[i]) and ("I-ORG" not in temp[i]) and ("E-ORG" not in temp[i]):
            temp[i] = temp[i]+' O'
    final = '\n'.join(temp)
    final_data_set.append(final)
    
train = final_data_set[:int(len(final_data_set)*0.9)]
dev = final_data_set[int(len(final_data_set)*0.9):]

f2=open("./train.txt",'w')
f2.write('\n\n'.join(train))
f2.close()

f3=open("./dev.txt",'w')
f3.write('\n\n'.join(train))
f3.close()
