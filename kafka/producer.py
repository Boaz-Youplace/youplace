from kafka import KafkaProducer
from json import dumps
import time

topic_name="boaz_youtube"
producer = KafkaProducer(
    acks=0,
    compression_type='gzip',
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')

)


start = time.time()
print("메시지 전송 시작")


for i in range(10000):
    data = {'str':'result'+str(i)}
    print("메시지 전송중..."+data['str'])
    producer.send(topic_name, value=data)
    producer.flush()
    
print("걸린시간 :",time.time()-start)