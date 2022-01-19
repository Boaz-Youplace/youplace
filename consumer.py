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
from collections import OrderedDict
import time
from ast import literal_eval


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

        # 파티션0 현재 offset num 저장
            p0_offset_before= self.consumer.committed(TopicPartition(self.topic_name,0))
            print(p0_offset_before,1)

        # 시간 측정
        start=time.time()

        # 한번 연결하고 계속 데이터를 가지고 올 것이기 때문에 무한루프로 실행
        while True :
            # last offset 기준으로 record 컨슘하기 - poll()
            msg_pack = self.consumer.poll(timeout_ms=500)
            self.consumer.commit()  
            # 파티션0 현재 offset num 저장
            p0_offset_after = self.consumer.committed(TopicPartition(self.topic_name,0))
            print(p0_offset_after,2)

            
            if p0_offset_after - p0_offset_before > 10 :
                with open('./json_files/test.json','w',encoding='utf-8') as f:
                    p0_offset_before=p0_offset_after
                    for tp, messages in msg_pack.items():
                        for message in messages:
                            data=literal_eval(message.value)
                            print(data)
                            print(type(data)) # dict 형태 
                            json.dump(data,f,ensure_ascii=False)
                            f.write('\n')
                            
                # for tp, messages in msg_pack.items():
                #     for message in messages:
                #         # pprint ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                #         #                                     message.offset, message.key,
                #         #                                     message.value))
                #         # # str ->json 변환 
                #         # tmp = json.loads(message.value)
                #         js=json.loads(message.value)

            # 5초 주기로 new record 확인 
            time.sleep(5)
            


if __name__ == '__main__':
    #basic_(제주 명소) : 총 6개
    basic_cg = KafkaConsumer_()
    basic_cg.set_group_id('con0116_8')
    basic_cg.set_topic_name('test0113')
    basic_cg.set_consumer()
    basic_cg._consume()

    