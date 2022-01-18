# -*- coding: utf-8 -*-
from tokenize import Double
import pymysql
from decimal import Decimal
import logging
import sys
import base64
import requests

def main():
    # headers = get_headers(client_id,client_secert)
    conn = pymysql.connect(host="boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com",user="admin",password="youplace",
            database="db_youplace",port=3306,use_unicode=True,charset ='utf8')
    # db = pymysql.connect(host='localhost', user='test', passwd='0000',db='youplace',charset='utf8')
    cursor = conn.cursor()
    print("DB connection success")

    # sql = '''
    # create table tb_youplace(
    #     id varchar(32) not null,
    #     place_name varchar(50) not null,
    #     viewCount int,
    #     publishTime varchar(50),
    #     likeCount int,
    #     x decimal(24,18),
    #     y decimal(24,18),
    #     category varchar(32),
    #     place_url varchar(100),
    #     address_6 varchar(32),
    #     primary key(id,place_name)
    #     )
    #     ''' 
    #     #engine = InnoEB default charset=utf8
    # cursor.execute(sql)

    data =[{"place_name": ["제주신화월드"], "x": ["126.31725882345"], "y": ["33.3060022512072"], "place_url": "http://place.map.kakao.com/829181290", "category": "숙박", "address_6": "서귀포시(서귀포시 중부)", "id": "ugnW1YC_waw", "publishTime": "2022-01-18T06:19:54Z", "likeCount": "2", "viewCount": "6"},{"place_name": ["9.81파크"], "x": ["126.36666400048769"], "y": ["33.39028982281912"], "place_url": "http://place.map.kakao.com/1868828759", "category": "관광,명소", "address_6": "애월,한림,한경(제주시 서부)", "id": "ugnW1YC_waw", "publishTime": "2022-01-18T06:19:54Z", "likeCount": "2", "viewCount": "6"},{"place_name": ["핑크뮬리"], "x": ["126.563648668769"], "y": ["33.2456830455915"], "place_url": "http://place.map.kakao.com/2022156809", "category": "가정,생활", "address_6": "서귀포시(서귀포시 중부)", "id": "ugnW1YC_waw", "publishTime": "2022-01-18T06:19:54Z", "likeCount": "2", "viewCount": "6"},{"place_name": ["올레길 16코스(고내-광령 올레)"], "x": ["126.38979561557086"], "y": ["33.46649759191228"], "place_url": "http://place.map.kakao.com/11943943", "category": "관광,명소", "address_6": "애월,한림,한경(제주시 서부)", "id": "4OmH_CSRn-8", "publishTime": "2022-01-17T16:39:38Z", "likeCount": "7", "viewCount": "20"},{"place_name": ["아르떼뮤지엄 제주"], "x": ["126.34501060259869"], "y": ["33.39670048068425"], "place_url": "http://place.map.kakao.com/1508345156", "category": "문화,예술", "address_6": "애월,한림,한경(제주시 서부)", "id": "4OmH_CSRn-8", "publishTime": "2022-01-17T16:39:38Z", "likeCount": "7", "viewCount": "20"}]


    # 다수의 데이터 삽입
    for d in data:
        # print(d['id'], d['place_name'][0], int(d['viewCount']), d['publishTime'], int(d['likeCount']), d['x'][0], d['y'][0], d['category'], d['place_url'], d['address_6'])
        sql = '''
        insert into tb_youplace(id,place_name,x,y,place_url,category,address_6,publishTime,likeCount,viewCount) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(sql,(d['id'],d['place_name'][0],Decimal(d['x'][0]),Decimal(d['y'][0]),d['place_url'],d['category'],d['address_6'],d['publishTime'],int(d['likeCount']),int(d['viewCount'])))
        
    conn.commit()

if __name__ == "__main__":
    main()