# -*- coding: utf-8 -*-
# 아주 잘된다네 ! 

from types import TracebackType
from kafka import KafkaConsumer
from kafka import TopicPartition

import json
import time

class KafkaConsumerExample:
    def __init__(self):
        self.host = 'localhost:9092'
        self.topic_name = 'partition_00'
        self.consumer = KafkaConsumer(bootstrap_servers=[self.host],
                                      # group_id='my-group3',
                                      auto_offset_reset='latest',
                                      enable_auto_commit=True, # 얘가 있으면 commit을 안해도 되는 거 아닌가?
                                      value_deserializer=lambda x: x.decode('utf-8'),
                                      consumer_timeout_ms=1000,
                                      )
        self.consumer.subscribe([self.topic_name])
        self.partitions = set()

    def _comsume(self):
      try: 
        # offset before,after partition별로 다 출력 찍기
        # broker가 더 있었다면 refactor도 있어야 했을것임...흑흑
        # 태빈님이 공유해주신 주키퍼 없는 카프카 도커 나중에 써봐도 좋을듯?
        
        # 시간측정
        start=time.time()
        print ('offset before =',self.consumer.committed(TopicPartition(self.topic_name, 0)))
        msg_pack = self.consumer.poll(timeout_ms=500)
        for tp, messages in msg_pack.items():
            for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                    message.offset, message.key,
                                                    message.value))
        
        self.consumer.commit()  # 컨슈밍이 완료되면 오프셋을 커밋한다.
        # print ('offset after =', self.consumer.committed(TopicPartition(self.topic_name, 0)))
        print('커밋완료!')
        print("걸린시간 :",time.time()-start)
      except:
          print('뭐냐 넌!')
          pass
          # self.rollback()  # 만약 에러가 생겼을때에는 롤백을 구현해준다.
          # 물론 아직 안만들었다..


if __name__ == '__main__':
    kafka = KafkaConsumerExample()
    kafka._comsume()