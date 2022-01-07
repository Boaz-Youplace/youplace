from kafka import KafkaProducer
from json import dumps
import time

topic_name="test_1" # 지금은 임의 설정 
producer = KafkaProducer(
    acks=0,
    compression_type='gzip',
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')

)



print(producer.partitions_for(topic_name))

start = time.time()
print("메시지 전송 시작")


for i in range(100):
    data = {'str':'result'+str(i)}
    print("메시지 전송중..."+data['str'])
    producer.send(topic_name, value=data)
    # 보내는 방식이 총 3가지 https://data-engineer-tech.tistory.com/14?category=847456 (비동기 send)
    producer.flush()
    
print("걸린시간 :",time.time()-start)



def on_send_success(record_metadata): 
    print(record_metadata.topic) 
    print(record_metadata.partition) 
    print(record_metadata.offset) 
    
def on_send_error(excp): 
    print(excp)