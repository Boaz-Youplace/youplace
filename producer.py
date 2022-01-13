# -*- coding: utf-8 -*-
'''
기능
1) 전처리 파일(data_processing.py) 실행 및 new records 획득
2) 토픽별로 KafkaProducer_ 객체 생성
3) new records 2)에 send
'''
from pprint import pprint
from kafka import KafkaProducer
from json import dumps
import time
import json
from bson import json_util
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
        print("메시지 전송 시작")
        start = time.time()
        for record in records:
            print("[",self.topic_name,"]에 메시지 전송중....")
            print(type(record))
            self.producer.send(self.topic_name,json.dumps(record,default=json_util.default).encode('utf-8'))
            # 보내는 방식이 총 3가지 https://data-engineer-tech.tistory.com/14?category=847456 (비동기 send)
            self.producer.flush()
        print("걸린시간 :",time.time()-start)

def on_send_success(record_metadata): 
    print(record_metadata.topic) 
    print(record_metadata.partition) 
    print(record_metadata.offset) 
    
def on_send_error(excp): 
    print(excp)
    
if __name__ == '__main__':
    # 1) 전처리 파일 실행 (인자 바꿔가며 수정) (입력값으로 바꿀지?)
    q='Jeju vlog'
    order='rating'
    max_result=5
    publishedAfter = None
    publishedBefore = None
    dataset = collect_data(q,order)
    records = data_processing_(dataset)
    pprint(records)

    print("----------------------------")
    #2) producer객체 topic개수만큼 생성 - 아직 안함
    #3) producer에 records 넣기
    test_producer = KafkaProducer_()
    test_producer.set_topic_name('test0113')
    test_producer._produce(records)
    
