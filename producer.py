# -*- coding:utf-8 -*-
'''
기능
1) 전처리 파일(data_processing.py) 실행 및 new records 획득
2) 토픽별로 KafkaProducer_ 객체 생성
3) new records 2)에 send
'''
from pprint import pprint
from kafka import KafkaProducer
from json import dumps
import yaml
import time
import json
# from bson import json_util
from data_processing import data_processing_
from collecting_data import collect_data


class KafkaProducer_:
    def __init__(self):
        self.host='localhost:9092'
        self.topic_name=''
        self.producer = KafkaProducer()
        
    def get_topic_name(self):
        return self.topic_name
    
    def set_topic_name(self,topic_name):
        self.topic_name = topic_name
    
    def set_producer(self):
        self.producer = KafkaProducer(
            acks=0,
            compression_type='gzip',
            bootstrap_servers=[self.host],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
    
    def get_partitions(self):
        partitions=self.producer.partitions_for_topic(self.topic_name)
        return partitions

    # send records
    def _produce(self,records):
        # 시간 측정
        print("메시지 전송 시작")
        start = time.time()
        print("[",self.topic_name,"]에 메시지 전송중....")
        for record in records:
            print(record)
            self.producer.send(self.topic_name, record)
            # 보내는 방식이 총 3가지 https://data-engineer-tech.tistory.com/14?category=847456 (비동기 send)
            self.producer.flush()
        print("전송완료")
        print("걸린시간 :",time.time()-start)

'''
    date – 리소스를 만든 날짜를 기준으로 최근 항목부터 시간 순서대로 리소스를 정렬합니다.
    rating – 높은 평가부터 낮은 평가순으로 리소스를 정렬합니다.
    videoCount – 업로드한 동영상 수에 따라 채널을 내림차순으로 정렬합니다.

    relevance – 검색 쿼리에 대한 관련성을 기준으로 리소스를 정렬합니다. 이 매개변수의 기본값입니다.
    title – 제목에 따라 문자순으로 리소스를 정렬합니다.
    viewCount – 리소스를 조회수가 높은 항목부터 정렬합니다.
'''
    

if __name__ == '__main__':
    querys = ['제주 Vlog','제주여행 브이로그','제주브이로그','제주도 브이로그','제주도 여행 브이로그','제주도 여행','제주 여행']
    orders = ['viewCount','rating']

    # 주기적으로 반복
    # while True :
    # for query in querys:
    #     for order in orders:
    publishedAfter=None
    publishedBefore=None
    dataset = collect_data('제주 브이로그','viewCount')
    records = data_processing_(dataset)
        
    print("데이터 개수: ",records[1]) #한번에 들어오는 레코드 개수


    # 시간 측정 for partitoin 없음
    start=time.time()
    producer = KafkaProducer_()
    producer.set_producer()
    producer.set_topic_name('youplace-part')
    producer._produce(records[0])
    print("파티션 10개일 때 걸린 시간: ",time.time()-start)


    # # 시간 측정 for partition -- 1
    # start=time.time()
    # producer_exp = KafkaProducer_()
    # producer_exp.set_producer()
    # producer_exp.set_topic_name('youplace')
    # producer._produce(records[0])
    # print("파티션 1개일 때 걸린 시간: ",time.time()-start)
        
   
