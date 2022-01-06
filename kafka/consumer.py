from kafka import KafkaConsumer
from json import loads
import time

# from kafka.structs import TopicPartition


topic_name="test"
consumer = KafkaConsumer (
    topic_name, 
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset = 'ealiest', ### 이놈이었음 ㅋ... 
    # enable_auto_commit=True, # 얘는 뭐징?
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000,
    )


start=time.time()
print("메시지 받아옴")

for message in consumer:
    print("partition", message.partition, "offset", message.offset, "value", message.value)
