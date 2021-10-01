from flask import Blueprint
'''
@app.route('/')라는 애너테이션이 url 매핑을 해주는 아이고, 이를 라우트 함수라고 한다.
그런데 이렇게 계속 데코레이터를 만들면 새로운 URL이 생길때마다 라우트함수를 계속 추가해야하는 불편함이 있다.
이때 사용할 수 있는 클래스가 블루프린트(blueprint)이다.
'''

bp = Blueprint('main',__name__,url_prefix='/')
# Blueprint 객체 생성 ( 이름, 모듈명, URL프리픽스 )

'''
애너테이션 ? 코드에 넣는 주석
URL 프리픽스 ? 접두어 URL을 정할 때 사용
'''

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return 'Pybo index'



# import threading, time

# from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
# from kafka.admin import NewTopic


# # run 시킬때마다 offset이 0으로 감 
# # 실제 브로커에 메시지가 저장되있는건 어떻게 해야하지? -> 파일시스템 
# # single-broker로 띄웠는데 이게 영향이 있을까?
# # flask에서도 잘 돌아갈까
# # 따로 데이터베이스는 안 둘 것인가? ( 파이프라인 관련 .. ) -> 구글 임포트,,,

# class Producer(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.stop_event = threading.Event()

#     def stop(self):
#         self.stop_event.set()

#     def run(self):
#         producer = KafkaProducer(bootstrap_servers='localhost:9092')

#         while not self.stop_event.is_set():
#             producer.send('my-topic', b"test")
#             producer.send('my-topic', b"\xc2Hola, mundo!")
#             time.sleep(1)

#         producer.close()
#         print("완.")

# # run 시킬때마다 offset이 0으로 감 
# # 실제 브로커에 메시지가 저장되있는건 어떻게 해야하지? -> 파일시스템 
# # single-broker로 띄웠는데 이게 영향이 있을까?
# # flask에서도 잘 돌아갈까
# # 따로 데이터베이스는 안 둘 것인가? ( 파이프라인 관련 .. ) -> 구글 임포트,,,

# class Consumer(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.stop_event = threading.Event()

#     def stop(self):
#         self.stop_event.set()

#     def run(self):
#         consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
#                                  auto_offset_reset='earliest',
#                                  consumer_timeout_ms=1000)
#         consumer.subscribe(['my-topic'])

#         while not self.stop_event.is_set():
#             for message in consumer:
#                 print(message)
#                 if self.stop_event.is_set():
#                     break

#         consumer.close()


# def main():
#     # Create 'my-topic' Kafka topic
#     try:
#         admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

#         topic = NewTopic(name='my-topic',
#                          num_partitions=1,
#                          replication_factor=1)
#         admin.create_topics([topic])
#     except Exception:
#         pass

#     tasks = [
#         Producer(),
#         Consumer()
#     ]

#     # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
#     for t in tasks:
#         t.start()

#     time.sleep(10)

#     # Stop threads
#     for task in tasks:
#         task.stop()

#     for task in tasks:
#         task.join()


# if __name__ == "__main__":
#     main()
