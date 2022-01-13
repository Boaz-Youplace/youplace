# -*- coding: utf-8 -*-
'''
기능
1) 전처리 파일(data_processing.py) 실행 및 새로운 데이터 kafkaProducer에 send
2) 토픽별로 KafkaProducer_ 객체 생성
'''
from pprint import pprint
from kafka import KafkaProducer
from json import dumps
import time
from ..data_processing import data_processing_
from ..collecting_data import collect_data

# 전처리 파일 실행 (인자 바꿔가며 수정)
# input 으로 넣을지?
q='Jeju vlog'
order='rating'
max_result=5
publishedAfter = ''
publishedBefore =''
dataset = collect_data(q,order,max_result,publishedAfter,publishedBefore)
records = data_processing_(dataset)
pprint(records)


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
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
    
    def get_partitions(self):
        partitions=self.producer.partitions_for_topic(self.topic_name)
        return partitions

    def _produce(self):
        print("메시지 전송 시작")
        start = time.time()
        for record in records:
            data=record
            print("메시지 전송중....")
            self.producer.send(self.topic_name,value=data)
            # 보내는 방식이 총 3가지 https://data-engineer-tech.tistory.com/14?category=847456 (비동기 send)
            self.producer.flush()
        print("걸린시간 :",time.time()-start)

def on_send_success(record_metadata): 
    print(record_metadata.topic) 
    print(record_metadata.partition) 
    print(record_metadata.offset) 
    
def on_send_error(excp): 
    print(excp)
    

test_producer = KafkaProducer_()
test_producer.set_topic_name('test')
    
