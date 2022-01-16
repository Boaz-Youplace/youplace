from ensurepip import bootstrap
from select import KQ_FILTER_AIO
from kafka import KafkaConsumer
from kafka import TopicPartition
from pprint import pprint
import time

topic_name = 'test0113'
consumer = KafkaConsumer(
    'test0113', 
    # group_id='plz..',
    bootstrap_servers='localhost:9092',
    enable_auto_commit=True, 
    # value_deserializer=lambda x: x.decode('utf-8'),
    auto_offset_reset='earliest')

# partitions = consumer.partitions_for_topic(topic_name)

# for p_id in partitions:
#     print('offset before =', consumer.committed(TopicPartition(topic_name,p_id)))

# start=time.time()


# msg_pack = consumer.poll(timeout_ms=500)

# for tp, messages in msg_pack.items():
#     for message in messages:
#     # message value and key are raw bytes -- decode if necessary!
#         # e.g., for unicode: `message.value.decode('utf-8')`
#         print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
#                                             message.offset, message.key,
#                                             message.value))
# consumer.commit()  # 컨슈밍이 완료되면 오프셋을 커밋한다.
    
# for p_id in partitions:
#     print('offset After =', consumer.committed(TopicPartition(topic_name,p_id)))

for message in consumer: 
    pprint("Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format( message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))

