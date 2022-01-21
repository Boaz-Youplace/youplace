# YouPlace
## Index
* 프로젝트 소개
* 프로젝트 참여자
* 파일 목록
* 기술 스택
* 기능 설명
* 추가 정보



## 프로젝트 소개
이젠 검색도 유튜브 시대 🎈

제주여행🌴을 계획할 때 브이로그 영상을 많이 참고하실텐데요 😊
수많은 영상들과 영상 속 분산된 명소들을 하나 하나 찾으려 생각하면 막막하지 않으셨나요? 😥😫

이러한 고민을 갖고 계신 분들을 위해, 유튜브 브이로거들이 찾아간 여행 명소들을 지도에서 한 눈에 파악할 수 있도록 만들었어요 💙


## 프로젝트 참여자
BOAZ DATA ENGINEERING 16TH
* 고은서
* 류정화
* 송경민

## 파일 목록
Youtube API를 통해 영상 데이터를 불러오고 전처리 진행 & 전처리에서 얻은 데이터로 Kakao API를 사용하여 장소 검색 => 각 영상에 나오는 장소 데이터들 추출
+ client-secret.json : GCP에서 발급한 Oauth2 사용자 인증 정보 json파일
+ collecting_data.py : Youtube API를 통해 영상 데이터 추출
+ consumer.py
+ consumer_multi_processing.py
+ data_processing.py : Youtube API를 통해 불러온 영상 데이터로 전처리 진행 & 전처리에서 얻은 데이터로 Kakao API를 사용하여 장소 검색 => 각 영상에 나오는 장소 데이터들 추출
+ google_apis.py : Youtube API의 search:list와 video:list API 연결코드
+ manage.py : Django 프로젝트 시작
+ original_consumer.py
+ producer.py
+ python_mySQL.py : python으로 MySQL연결하는 코드 (사전에 사용자 생성 후 권한 부여해줘야함)
+ rds_create_table.py : AWS RDS의 DB에 연결 후 테이블 생성하는 코드
+ rds_insert_data.py : AWS RDS DB의 테이블에 데이터 삽입하는 코드
+ requirements.txt
+ spark-convert-df.py

## 기술 스택
##### 버전정보
* kafka:
* spark:

## 기능 설명
> 데이터 파이프라인  
유튜브 API(+카카오API) → 카프카 →  스파크 SQL →  DB → 스파크 SQL → 장고 (웹)
1. 유튜브 API로 제주 브이로그 관련 영상 데이터 수집 후 전처리 진행 & Kakao API를 통해 장소 정보도 수집
2. 전처리한 영상 정보와 장소 정보가 담긴 데이터를 카프카 프로듀서와 연결(토픽 1개)
3. 카프카 컨슈머에서 받음
4. 스파크에서 이 데이터를 받아서 데이터 형태를 JSON → RDD 형태로 변환(기능 : 다량의 데이터를 효과적으로 처리)
5. MySQL에 적재
6. MySQL에 있는 데이터들을 활용해 스파크 SQL에서 통계처리
7. Django를 통해 웹페이지 생성

## 추가 정보
* notion: https://prickle-ragdoll-392.notion.site/BOAZ-ONLINE-CONFERENCE-2022-c4803bfc11db4bc58e2ad0f1903163fb
* slideshare:
* youtube:
* web: 추후 배포 예정
