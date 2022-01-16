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
    
    # 파티션0 기준으로 offset 차이가 100이상 나는지 확인
    def compare_offset_diffrence(self,os_before,os_now):
        if os_now-os_before >50 :
            return True
        return False

    def _consume(self):
        partitions = self.get_partitions()

        # 파티션 별 last offset 읽기
        for p_id in partitions:
            print ('offset %d before = %d' %(p_id,self.consumer.committed(TopicPartition(self.topic_name, p_id))))

        # 시간 측정
        start=time.time()


        # 한번 연결하고 계속 데이터를 가지고 올 것이기 때문에 무한루프로 실행
        while True :
            # 파티션0 현재 offset num 저장
            p0_offset_before = self.consumer.committed(TopicPartition(self.topic_name,0))
            print(p0_offset_before)

            # last offset 기준으로 record 컨슘하기 - poll()
            msg_pack = self.consumer.poll(timeout_ms=500)

            # 파티션0 현재 offset num 저장
            p0_offset_after = self.consumer.committed(TopicPartition(self.topic_name,0))
            print(p0_offset_after)

            # 파티션0 offset num 차이 비교
            if self.compare_offset_diffrence(p0_offset_before,p0_offset_after) :
                # json 파일 만들기
                pass


            for tp, messages in msg_pack.items():
                for message in messages:
                    # message value and key are raw bytes -- decode if necessary!
                    # e.g., for unicode: `message.value.decode('utf-8')`
                    pprint ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                        message.offset, message.key,
                                                        message.value))
                    print(type(message.value))
                    # str ->json 변환 
                    tmp = json.loads(message.value)
                    print(tmp)
                    print(tmp['place_name'])
        


if __name__ == '__main__':
    #basic_(제주 명소) : 총 6개
    basic_cg = KafkaConsumer_()
    basic_cg.set_group_id('con0116_8')
    basic_cg.set_topic_name('test0113')
    basic_cg.set_consumer()
    basic_cg._consume()

    