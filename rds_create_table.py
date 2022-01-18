# -*- coding: utf-8 -*-
from tokenize import Double
import pymysql
from decimal import Decimal
import logging
import sys
import base64
import requests

def main():
    conn = pymysql.connect(host="boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com",user="admin",password="youplace",
            database="db_youplace",port=3306,use_unicode=True,charset ='utf8')
    # db = pymysql.connect(host='localhost', user='test', passwd='0000',db='youplace',charset='utf8')
    cursor = conn.cursor()
    print("DB connection success")

    sql = '''
    create table tb_youplace(
        id varchar(32) not null,
        place_name varchar(50) not null,
        viewCount int,
        publishTime varchar(50),
        likeCount int,
        x decimal(24,18),
        y decimal(24,18),
        category varchar(32),
        place_url varchar(100),
        address_6 varchar(32),
        primary key(id,place_name)
        )
        ''' 
        #engine = InnoEB default charset=utf8
    cursor.execute(sql)