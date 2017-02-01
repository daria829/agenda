# created by Tanaka Takuma on 2017/01/25 
# -*- coding: utf-8 -*-

import re
import os
import csv
import kan_to_arab as kta #漢数字をアラビア数字に変換するスクリプト
import database

ends = ["条例", "について", "の件", "上程", "予算"]
multi = ["並び", "及び", "ならび", "および", "ないし", "、"]

def get_from_index(file):
    csvfile = open(file, "rt")
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')

    #データーベースに接続
    db = database.Database()
    db.Connect_Database("agenda")
    
    #テーブル作成
    #match = re.match(r'.+list/(.+?)_list.csv', file)
    #name = match.group(1) 
    #create_table(db, name)
    
    i = 0
    se_list = []
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
                     y = 0
                     m = 0
                     d = 0
                 else:
                     y = int(match.group(1))
                     m = int(match.group(2))
                     d = int(match.group(3))
                 
                 sql = "INSERT INTO %s (JITITAI_MEI, KAISAI_NEN, KAISAI_TSUKI, KAISAI_HI, KAIGI_MEI, GIAN_BANGOU, GIDAI_MEI)" % name + \
                         "VALUES ('%s', %d, %d, %d, '%s', %d, '%s');" % (r[0], y, m, d, r[4], agenda_num, agenda_title) 
                 #db.ExeSQL(sql)            
                 #db.Commit()
    db.Close_Database()

#テーブルを作成
def create_table(object, name):
    sql = "CREATE TABLE %s (" % name + \
          "JITITAI_MEI varchar(30)," + \
          "KAISAI_NEN int," + \
          "KAISAI_TSUKI int," + \
          "KAISAI_HI int," + \
          "KAIGI_MEI varchar(90)," + \
          "GIAN_BANGOU int," + \
          "GIDAI_MEI text" + \
          ");"
    object.ExeSQL(sql)

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

#議案番号が複数あるかチェック
def check_multi(text):
    for m in multi:
        if m in text:
            return False
    return True

# 目次中の議案名を抽出
def get_from_index(text):
    text = text.strip()
    text_list = text.split()
    
    if len(text_list) == 2:
        match = re.match(r"第([0-9０-９]+?)号.*", text_list[0])
        if match is None:
            print(text_list[1])
            match = re.match(r".+（議案第([0-9０-９]+)号）.*", text_list[1])
            if match is None:
                pass 
            else:
                print(match.group(1), text_list[1])
            return 0, 0
        elif check_multi(text_list[0]):
            agenda_num = int(match.group(1))
            agenda_title = text_list[1]
            return agenda_num, agenda_title
        else:
            return 0, 0

    elif len(text_list) == 3:
        match = re.match(r".*議第([0-9０-９]+)号.*", text_list[1])
        if match is None:
            return 0, 0
        elif len(text_list) == 3 and check_multi(text_list[1]):
            agenda_num = int(match.group(1))
            agenda_title = text_list[2] 
            return agenda_num, agenda_title
        else:
            return 0, 0
    else:
        return 0, 0
    
        
        
# 本文から議案が入った一文をリストにいれて返す
def get_about_agenda(text):
    text_list = text.split("\n")
    se_list = []
    for se in text_list:
        if "議案" in se or "議第" in se:
            se_list.append(se)
    return se_list
            
        
if __name__=="__main__" :
    csv_list = os.listdir('/home/t-tanaka/Documents/list/')
    i = 0
    end_csv_list = ["miyagi_list.csv", "nigata_list.csv", "yamagata_list.csv", "kochi_list.csv"]
    for file in csv_list:
        if ".csv" in file and file not in end_csv_list:
            i+=1
            print(file+"#"+str(i)+"****************************************************")
            csv_get("/home/t-tanaka/Documents/list/" + file)
            
