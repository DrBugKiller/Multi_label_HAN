# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 15:40
# @Author  : DrMa
import psycopg2
import json
from tqdm import tqdm,trange

def todic(list):  # 给定二维list,构建字典
    dic = {}
    for l in list:
        dic[l[0]] = l[1]  # key值对应value
    return dic

def getdics(cur):  # 工作，教育程度，民族，审判程序，性别，刑法类别，罪名，省市县。{值：代号}
    cur.execute("select value, key from dic where type = 'gz'")
    gz = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'jycd'")
    jycd = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'mz'")
    mz = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'spcx'")
    spcx = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'gz'")
    xb = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'xflb'")
    xflb = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'zm'")
    zm = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'sheng'")
    sheng = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'shi'")
    shi = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'xian'")
    xian = todic(cur.fetchall())
    cur.execute("select value, key from dic where type = 'wslx'")
    wslx = todic(cur.fetchall())
    return gz, jycd, mz, spcx, xb, xflb, zm, sheng, shi, xian, wslx

def get_multi_charge_from_db(table_name):
    sql = "select zm,fzss from " + table_name + " where zm like '%,%' limit 1000"
    conn = psycopg2.connect(database='justice', user='beaver', password='123456', host='58.56.137.206', port='5432')
    print('connected successfully!')
    cur = conn.cursor()
    cur.execute(sql)
    ws_s = cur.fetchall()
    for ws in ws_s:
        print(ws[1], '\n\n')
        print(ws[0].split(','))

# get_multi_charge_from_db('bgrspb_xx_test3')
def get_multi_charge_from_CAIL(json_name,out_file_name):
    f = open(json_name, 'r+', encoding='utf-8')
    json_str = f.readlines()
    f.close()
    index = 0
    f=open(out_file_name,'w+',encoding='utf-8')
    for i in tqdm(json_str):
        temp_dict = json.loads(i)  # dict

        fact = temp_dict['fact']  # 犯罪事实,str
        relevant_articles = temp_dict['meta']['relevant_articles']  # 法条,list,可能有多个
        accusation = temp_dict['meta']['accusation']  # 罪名,list,可能有多个
        punish_of_money = temp_dict['meta']['punish_of_money']  # 罚金,int,只有一个
        criminals = temp_dict['meta']['criminals']  # 罪犯,list,可能有多个
        term_of_imprisonment = temp_dict['meta']['term_of_imprisonment']  # 刑期,字典
        death_penalty = term_of_imprisonment['death_penalty']  # 是否死刑,bool
        imprisonment = term_of_imprisonment['imprisonment']  # 有期徒刑,几个月,int
        life_imprisonment = term_of_imprisonment['life_imprisonment']  #是否无期徒刑,bool

        if len(accusation)>1:
            for j in range(len(criminals)):
                fact=fact.replace(criminals[j],'AA'+str(j))
            f.write('#'.join(accusation)+'\n'+fact+'\n\n')#+fact+'\n\n'
            index+=1
    print(index)
    f.close()
namelist=[['.\data\data_train.json','.\data\\train_fact.txt'],
          ['.\data\data_test.json','.\data\\test_fact.txt'],
          ['.\data\data_valid.json','.\data\\valid_fact.txt']]
def save_multi_doc(namelist):#写入本地
    for i in namelist:
        get_multi_charge_from_CAIL(i[0],i[1])

save_multi_doc(namelist)



def get_zm_dict(train,test,valid):
    #zm to index
    #拿到每个罪名,对应的频次. 一共有200项罪名
    zm_dic={}
    zm_s=[]
    namelist=[train,test,valid]
    for i in namelist:
        f=open(i,'r+',encoding='utf-8')
        lines=f.read().split('\n')
        f.close()
        for line in tqdm(lines):
            zm_list=line.split('#')#.split('\n')[0]
            if zm_list!=['']:
                zm_s.extend(zm_list)
    for zm in zm_s:
        if not zm in zm_dic:
            zm_dic[zm]=1
        else:
            zm_dic[zm]+=1
    zm_name_count=list(zip(zm_dic.keys(),zm_dic.values()))
    zm_name_count.sort(key=lambda s:s[1],reverse=True)#sort的高端用法
    zm_dic={}
    for i in zm_name_count:
        zm_dic[i[0]]=len(zm_dic)
    return zm_dic

# zm_dic=get_zm_dict('.\data\\train_fact.txt','.\data\\test_fact.txt','.\data\\valid_fact.txt')
def save_zm_dic(zm_dic,zm_dic_file):
    f=open(zm_dic_file,'w+',encoding='utf-8')
    temp_dic_str=json.dumps(zm_dic,ensure_ascii=False)
    f.write(temp_dic_str)
    f.close()
# save_zm_dic(zm_dic,'.\data\\zm_dic.json')
def load_zm_dic(zm_dic_file):
    f=open(zm_dic_file,'r+',encoding='utf-8')
    zm_dic=json.loads(f.read())
    f.close()
    return zm_dic
zm_dic=load_zm_dic('.\data\\zm_dic.json')
