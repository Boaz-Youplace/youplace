# https://data-newbie.tistory.com/238?category=761014

# consumer.py에서 while True문 제거 -> poll() 이후 기다리지 않고 바로 시간 측정해보기 (base)
# multi_processing을 통한 파티션별 독립적으로 작업 수행 -> 시간 더 단축? (adv)

# -> partition을 여러개로 두었을 때 얼만큼의 시간차이가 나는 지 비교할 수 있음 

# -*- coding: utf-8 -*-
'''
기능
1) 토픽별로 KafkaConsumer_ 객체(Consumer Group) 생성
'''
from encodings import utf_8
from ensurepip import bootstrap
from select import KQ_FILTER_AIO
from kafka import KafkaConsumer
from kafka import TopicPartition
from pprint import pprint
import json

import time

class KafkaConsumer_:
    def __init__(self):
        self.host = 'localhost:9092'
        self.topic_name = ''
        self.group_id = ''
        self.consumer = KafkaConsumer()
        self.partitions = set()
        
    def set_consumer(self):
        self.consumer = KafkaConsumer( 
            self.topic_name,
            bootstrap_servers=[self.host],
            group_id=self.group_id,
            auto_offset_reset='latest',
            enable_auto_commit=True, 
            value_deserializer=lambda x: x.decode('utf-8'),
            consumer_timeout_ms=100000,
        )
        
    def set_group_id(self,group_id):
        self.group_id=group_id
    
    def get_group_id(self):
        return self.group_id
        
    def set_host(self,host):
        self.host = host
        
    def get_host(self):
        return self.host
    
    def set_topic_name(self,topic_name):
        self.topic_name = topic_name
    
    def get_topic_name(self):
        return self.topic_name

    def get_partitions(self):
        partitions=self.consumer.partitions_for_topic(self.topic_name)
        return partitions
    
    def _consume(self):
        partitions = self.get_partitions()
        
        # 파티션 별 last offset 읽기
        for p_id in partitions:
            print ('offset %d before = %d' %(p_id,self.consumer.committed(TopicPartition(self.topic_name, p_id))))

        # 시간 측정
        start=time.time()


        # record 뽑아오기(일회성)
        msg_pack = self.consumer.poll(timeout_ms=500)
        
        # 컨슈밍이 완료되면 오프셋 수동 커밋 (커밋 옵션이 5초 주기이기 때문에 일회성으로 뽑으면 자동 커밋 안됨 )
        self.consumer.commit()  
        print('커밋완료!')

        # 시간 측정 완료
        for p_id in partitions:
            print ('offset %d after = %d' %(p_id,self.consumer.committed(TopicPartition(self.topic_name,p_id))))
            
        
        print("걸린시간 :",time.time()-start)


if __name__ == '__main__':
    #basic_(제주 명소) : 총 6개
    basic_cg = KafkaConsumer_()
    basic_cg.set_group_id('con0116_8')
    basic_cg.set_topic_name('test0113')
    basic_cg.set_consumer()
    basic_cg._consume()
