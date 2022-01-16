# -*- coding: utf-8 -*-
'''
기능
1) 토픽별로 KafkaConsumer_ 객체(Consumer Group) 생성
'''
from ensurepip import bootstrap
from select import KQ_FILTER_AIO
from kafka import KafkaConsumer
from kafka import TopicPartition


import time

class koeunseo:
    def __init__(self):
        self.host = 'localhost:9092'
        self.topic_name = ''
        self.group_id = 'sr'
        self.consumer = KafkaConsumer()
        # self.consumer.subscribe([self.topic_name])
        self.partitions = set()
        
    def set_consumer(self):
        self.consumer = KafkaConsumer( 
            bootstrap_servers=[self.host],
            group_id=self.group_id,
            auto_offset_reset='latest',
            enable_auto_commit=True, # 얘가 있으면 commit을 안해도 되는 거 아닌가?
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
        print(self.consumer.topics())
        # self.consumer.subscribe([self.topic_name])

        print(self.consumer.subscribe(self.topic_name),1)
        print(self.consumer.subscription(),11)
        
        partitions = self.get_partitions()
        print(partitions,444)
        
        for p_id in partitions:
            print ('offset before =',self.consumer.committed(TopicPartition(self.topic_name, p_id)))
        # 시간 측정
        start=time.time()

        try:
            while True:
                msg_pack=self.consumer.poll(timeout_ms=10000)
                for tp,msgs in msg_pack.items():
                    for msg in msgs:
                        print("%s:%d:%d: value=%s" % (tp.topic,tp.partition,msg.offset,msg.value))
        finally:
            self.consumer.close()
        # 이거 mac에서만 안되는 건지 확인해볼 필요가 있음..
        # msg_pack = self.consumer.poll(timeout_ms=500)
        # while True:
            # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
        # msg_pack = self.consumer.poll(timeout_ms=500)

        # for tp, messages in msg_pack.items():
        #     for message in messages:
        #         # message value and key are raw bytes -- decode if necessary!
        #         # e.g., for unicode: `message.value.decode('utf-8')`
        #         print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
        #                                             message.offset, message.key,
        #                                             message.value))
        # self.consumer.commit()  # 컨슈밍이 완료되면 오프셋을 커밋한다.
        for p_id in partitions:
            print ('offset after =', self.consumer.committed(TopicPartition(self.topic_name, p_id)))
            
        print('커밋완료!')
        print("걸린시간 :",time.time()-start)


if __name__ == '__main__':
    #basic_(제주 명소) : 총 6개
    basic_cg = koeunseo()
    basic_cg.set_group_id('con0116_8')
    basic_cg.set_topic_name('test0113')
    basic_cg.set_consumer()
    basic_cg._consume()

