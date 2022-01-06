from kafka import KafkaConsumer
from json import loads
import time

topic_name="partition_0"
consumer = KafkaConsumer (
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset = 'earliest',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000
    )

start=time.time()
print("메시지 받아옴",topic_name)

for message in consumer :
    print("partition", message.partition, "offset", message.value)