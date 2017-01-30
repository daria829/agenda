# database.py
# created by Tanaka Takuma on 2016/07/15 
# -*- coding: utf-8 -*-

import mysql.connector
import time

class Database:
    # データベースに接続
    def Connect_Database(self, database_name):
        self.connector = mysql.connector.connect(host = "localhost",
                                    database = database_name,
                                    user = "root",
                                    password = "pass",
                                    charset = "utf8")
        self.cursor = self.connector.cursor()
    
    # データベースとの接続をクローズ
    def Close_Database(self):
        self.cursor.close()
        self.connector.close()

    # 命令をコミット
    def Commit(self):
        self.connector.commit()

    # データベースにインサート
    def Insert_Item(self, table, object):
        try:
            query = "INSERT INTO " + table +  "(NAME, USR_ID, KAIGI_ID, HATSUGEN_ID, TITLE, HATSUGEN, URL, category, date, hatsugensya, yakusyoku) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            self.cursor.execute(query, (object.name, object.usr_id, object.kaigi_id, object.hatsugen_id,
                                        object.title, object.hatsugen, object.url, object.category,
                                        object.date, object.hatsugensya, object.yakusyoku))
           
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    # データベースにインサート
    def new_Insert_Item(self, table, object):
        try:
            query = "INSERT INTO " + table +  "(HATSUGEN_ID, JITITAI_MEI, KAI, GOU, KAISAI_NEN, KAISAI_TSUKI, KAISAI_HI, KAISAI_NISSU, KAIGI_MEI, HATSUGENSYA_SYURUI, HATSUGENSYA_ID, HATSUGENSYA, YAKUSYOKU, HATSUGEN, HATSUGEN_OTHER, URL, HTML_FILE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            self.cursor.execute(query, (object.hatsugen_id, object.jititai_mei, object.kai, object.gou,
                                        object.kaisai_nen, object.kaisai_tsuki, object.kaisai_hi, object.kaisai_nissu, 
					object.kaigi_mei, object.hatsugensya_syurui, object.hatsugensya_id, object.hatsugensya, 
					object.yakusyoku, object.hatsugen, object.hatsugen_other, object.url, object.html_file))
           
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    # SQL文を実行してその結果を返す
    def GetSQLRows(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return []

    # SQL文を実行する
    def ExeSQL(self, query):
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        
    def Create_Table(self, table_name):
        try:
            query = "CREATE TABLE %s(NAME varchar(90),USR_ID varchar(90), KAIGI_ID int, HATSUGEN_ID varchar(90), TITLE varchar(90), HATSUGEN mediumtext, URL text, hatsugensya varchar(90), category varchar(90), date varchar(90), yakusyoku varchar(90));" % table_name
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return []

    def new_Create_Table(self, table_name):
        try:
            query = "CREATE TABLE %s(" % table_name + \
                    "HATSUGEN_ID varchar(30)," + \
                    "JITITAI_MEI varchar(30)," + \
                    "KAI int," + \
                    "GOU int," + \
                    "KAISAI_NEN int," + \
                    "KAISAI_TSUKI int," + \
                    "KAISAI_HI int," + \
		    "KAISAI_NISSU int," + \
                    "KAIGI_MEI varchar(90)," + \
                    "HATSUGENSYA_SYURUI varchar(10)," + \
		    "HATSUGENSYA_ID varchar(30)," + \
                    "HATSUGENSYA text," + \
                    "YAKUSYOKU varchar(50)," + \
                    "HATSUGEN mediumtext," + \
                    "HATSUGEN_OTHER mediumtext," + \
                    "URL text," + \
                    "HTML_FILE text" + \
                    ");"
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return []
        
