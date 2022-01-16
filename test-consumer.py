from kafka import KafkaConsumer
from kafka import TopicPartition
from pprint import pprint 

consumer = KafkaConsumer('test0113', bootstrap_servers='localhost:9092',
enable_auto_commit=True, auto_offset_reset='earliest')

for message in consumer: 
    pprint("Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format( message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))