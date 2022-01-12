# -*- coding: utf-8 -*-
# 토픽별 컨슈머 그룹도 다 다르니까 클래스로 관리하는 게 편할 거임

from kafka import KafkaConsumer
from kafka import TopicPartition


import time

class KafkaConsumer_:
    def __init__(self):
        self.host = 'localhost:9092'
        self.topic_name = ''
        self.group_id = ''
        self.consumer = KafkaConsumer()
        # self.consumer.subscribe([self.topic_name])
        self.partitions = set()
        
    def set_consumer(self):
        self.consumer = KafkaConsumer(bootstrap_servers=[self.host],
                                      group_id=self.group_id,
                                      auto_offset_reset='latest',
                                      enable_auto_commit=True, # 얘가 있으면 commit을 안해도 되는 거 아닌가?
                                      value_deserializer=lambda x: x.decode('utf-8'),
                                      consumer_timeout_ms=1000,
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
      try: 
        # broker가 더 있었다면 refactor도 있어야 했을것임
        # 태빈님이 공유해주신 주키퍼 없는 카프카 도커 나중에 써봐도 좋을듯?
        consumer=self.consumer
        consumer.subscribe([self.topic_name])
        
        partitions = self.get_partitions()
        
        for p_id in partitions:
            print ('offset before =',self.consumer.committed(TopicPartition(self.topic_name, p_id)))
        # 시간 측정
        start=time.time()
        msg_pack = self.consumer.poll(timeout_ms=500)
        # print(msg_pack)
        for tp, messages in msg_pack.items():
            for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                    message.offset, message.key,
                                                    message.value))
        
        self.consumer.commit()  # 컨슈밍이 완료되면 오프셋을 커밋한다.
        for p_id in partitions:
            print ('offset after =', self.consumer.committed(TopicPartition(self.topic_name, p_id)))
            
        print('커밋완료!')
        print("걸린시간 :",time.time()-start)
      except:
          pass
          # self.rollback()  # 만약 에러가 생겼을때에는 롤백을 구현한다.
          # 아직 안만듬


if __name__ == '__main__':
    #consumer group 2개로 나누기. basic과 stat(통계)
    basic_cg = KafkaConsumer_()
    basic_cg.set_group_id('220112')
    basic_cg.set_topic_name('boaz_youtube_2')
    basic_cg.set_consumer()
    basic_cg._consume()
    
    # 실행은 consumer_group.py에서!