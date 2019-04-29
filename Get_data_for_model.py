# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 20:31
# @Author  : DrMa
import jieba
from get_doc import load_zm_dic
import collections
from tqdm import tqdm
jieba.load_userdict('./data/user_dict.txt')
def jieba_user_dict(file):
    f=open(file,'w+',encoding='utf-8')
    zm_dic = load_zm_dic('.\data\\zm_dic.json')
    zms=zm_dic.keys()
    for zm in zms:
        f.write(zm+'\n')
    f.write('AA0'+'\n'+'AA1')
    f.close()

def get_word_dict(train,test,valid,low_count=None):
    name_list=[train,test,valid]
    txt=[]
    for name in name_list:
        f=open(name,'r+',encoding='utf-8')
        lines=f.read().strip('\n\n').split('\n\n')
        f.close()
        for line in tqdm(lines):
            fact=line.split('\n')[1]
            words=list(jieba.cut(fact))
            txt.extend(words)
    word_count=collections.Counter(txt)

    print(word_count)
get_word_dict('./data/test_fact.txt','./data/test_fact.txt','./data/test_fact.txt')

