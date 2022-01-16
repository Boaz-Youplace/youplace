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

        # record 뽑아오기
        # msg_pack = self.consumer.poll(timeout_ms=500)

        # 한번 연결하고 계속 데이터를 가지고 올 것이기 때문에 무한루프로 실행
        while True :
            msg_pack = self.consumer.poll(timeout_ms=500)
            for tp, messages in msg_pack.items():
                for message in messages:
                    # message value and key are raw bytes -- decode if necessary!
                    # e.g., for unicode: `message.value.decode('utf-8')`
                    pprint ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                        message.offset, message.key,
                                                        message.value))
                    print(message.value)
                    print(type(message.value))
                    tmp = json.loads(message.value)
                    print(tmp)
                    print(tmp['place_name'])
        
        # 컨슈밍이 완료되면 오프셋 커밋 -> 아래 코드는 consumer_multi_processing함수에서 진행
        # self.consumer.commit()  
        # print('커밋완료!')

        # # 시간 측정 완료
        # for p_id in partitions:
        #     print ('offset %d after = %d' %(p_id,self.consumer.committed(TopicPartition(self.topic_name,p_id))))
            
        
        # print("걸린시간 :",time.time()-start)


if __name__ == '__main__':
    #basic_(제주 명소) : 총 6개
    basic_cg = KafkaConsumer_()
    basic_cg.set_group_id('con0116_8')
    basic_cg.set_topic_name('test0113')
    basic_cg.set_consumer()
    basic_cg._consume()

    