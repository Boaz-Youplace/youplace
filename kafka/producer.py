from kafka import KafkaProducer
from json import dumps
import time

topic_name="partition_00"
producer = KafkaProducer(
    acks=0,
    compression_type='gzip',
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')

)



print(producer.partitions_for(topic_name),222)

start = time.time()
print("메시지 전송 시작")


for i in range(100):
    data = {'str':'result'+str(i)}
    print("메시지 전송중..."+data['str'])
    producer.send(topic_name, value=data)
    # .add_callback(on_send_success).add_errback(on_send_error) 
    # 보내는 방식이 총 3가지가 있다고 함. 그 중 마지막 방식 사용 https://data-engineer-tech.tistory.com/14?category=847456 (비동기 send)
    producer.flush()
    
print("걸린시간 :",time.time()-start)



def on_send_success(record_metadata): 
    print(record_metadata.topic) 
    print(record_metadata.partition) 
    print(record_metadata.offset) 
    
def on_send_error(excp): 
    print(excp)