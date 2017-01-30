# ajenda.py
# created by Tanaka Takuma on 2017/01/25 
# -*- coding: utf-8 -*-

import re
import os
import csv
import kan_to_arab as kta #漢数字をアラビア数字に変換するスクリプト
import database

ends = ["条例", "について", "の件", "上程", "予算"]

def csv_get(file):
    csvfile = open(file, "rt")
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    se_list = []

    #データーベースに接続
    db = database.Database()
    db.Connect_Database("ajenda")
    
    #テーブルを作成
    sql = "CREATE TABLE %s(" % file \
          "JITITAI_MEI varchar(30)," \
          "KAISAI_NEN int,"\
          "KAISAI_TSUKI int,"\
          "KAISAI_HI int,"\
          "KAIGI_MEI varchar(90),"\
          "GIAN_BANGOU int,"\
          "GIDAI_MEI text,"\
          ");"
    db.ExeSQL(sql)
    i = 0
    for r in rows:
        if len(r) < 5:
            continue
        for se in get_about_agenda(r[5]):
            i+=1
            se = kta.kansuji2arabic(se, True)
            agenda_num, agenda_title = get_from_index(se)
            if agenda_num != 0:
                 match = re.match(r".*平成([0-9０-９]+?)年.*([0-9０-９]+?)月([0-9０-９]+?)日.*?", r[4])
                 if match is None:
                     pass
                 else:
                     y = int(match.group(1))
                     m = int(match.group(2))
                     d = int(match.group(3))
                     print(r[4])
                     print(y,m,d)
      
     db.DisConnect_Database()
            
def num_to_num(text):
    match = re.match(r".*第([0-9０-９]+?)号から第([0-9０-９]+?)号.*", text)
    if match is None:
        return 0, 0
    else:
        s = int(match.group(1))
        e = int(match.group(2))
    return s, e

def num_content(text):
    return re.match(r".*?議案*第[0-9０-９]+?号", text)

# 目次中の議案名を抽出
def get_from_index(text):
    text = text.strip()
    text_list = text.split()
    if 2 > len(text_list) or 3 < len(text_list):
        return 0, 0
    match = re.match(r"第([1-9１-９]+)号", text_list[0])
    if match is None:
        return 0, 0
    else:
        agenda_num = int(match.group(1))
        agenda_title = text_list[1]
        return agenda_num, agenda_title

    
        
        
# 本文から議案が入った一文をリストにいれて返す
def get_about_agenda(text):
    text_list = text.split("\n")
    se_list = []
    for se in text_list:
        if "議案" in se or "議第" in se:
            se_list.append(se)
    return se_list
            
        
if __name__=="__main__" :
    csv_list = os.listdir('/Users/t-tanaka/Documents/list/')
    i = 0
    csv_list = ["saitama_list.csv","nigata_list.csv","kochi_list.csv","miyagi_list.csv", "yamagata_list.csv"]
    for file in csv_list:
        if ".csv" in file:
            i+=1
            print(file+"#"+str(i)+"****************************************************")
            csv_get("/Users/t-tanaka/Documents/list/" + file)
            
