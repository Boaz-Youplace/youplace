# YouPlaceπΊοΈπ
**μΉ΄νμΉ΄**μ **μ€νν¬**λ₯Ό νμ©ν **μ νλΈ μμ** μ **μ μ£Ό λͺμ κ²μ**


## 1. νλ‘μ νΈ μκ°
μ΄μ   κ²μλ μ νλΈ μλ π

μ μ£Όμ¬νπ΄μ κ³νν  λ λΈμ΄λ‘κ·Έ μμμ λ§μ΄ μ°Έκ³ νμ€νλ°μ π
μλ§μ μμλ€κ³Ό μμ μ λΆμ°λ λͺμλ€μ νλ νλ μ°ΎμΌλ € μκ°νλ©΄ λ§λ§νμ§ μμΌμ¨λμ? π₯π«

μ΄λ¬ν κ³ λ―Όμ κ°κ³  κ³μ  λΆλ€μ μν΄, μ νλΈ λΈμ΄λ‘κ±°λ€μ΄ μ°Ύμκ° μ¬ν λͺμλ€μ μ§λμμ ν λμ νμν  μ μλλ‘ λ§λ€μμ΄μ π

## 2. κΈ°μ  μ€ν
+ Cloud : AWS EC2, Docker  
+ Engineering : Kafka, Spark  
+ DB & Web : MYSQL(RDS), Django  

## 3. νμ΄νλΌμΈ μκ°
> λ°μ΄ν° νμ΄νλΌμΈ  
μ νλΈ API(+μΉ΄μΉ΄μ€API) β μΉ΄νμΉ΄ β  μ€νν¬ SQL β  DB β μ€νν¬ SQL β μ₯κ³  (μΉ)
1. μ νλΈ APIλ‘ μ μ£Ό λΈμ΄λ‘κ·Έ κ΄λ ¨ μμ λ°μ΄ν° μμ§ ν μ μ²λ¦¬ μ§ν & Kakao APIλ₯Ό ν΅ν΄ μ₯μ μ λ³΄λ μμ§
2. μΉ΄νμΉ΄ μλ² κ΅¬μΆ
3. μΉ΄νμΉ΄ νλ‘λμ λ¨ - μ μ²λ¦¬ν λ°μ΄ν°λ€μ ν ν°ννμ¬ μ νλΈ apiμ producer μ°κ²° μμμ μν + producer κ°μ²΄λ₯Ό ν ν½ κ°μλ§νΌ μμ±μ ν ν λ μ½λμ λ£λ μμμ μν
4. μΉ΄νμΉ΄ μ»¨μλ¨Έλ¨ - νλ‘λμ λ¨κ³Ό λ°μ΄ν°νμμ λ§μΆκΈ° μν μ²λ¦¬ κ³Όμ μ μν
5. μΉ΄νμΉ΄ Consumerμ Spark μ°κ²°
6. μ€νν¬μμ μ΄ λ°μ΄ν°λ₯Ό λ°μμ Mysql DB μ½μμ μν νν λ³ν μμ μν(λ°μ΄ν° ννλ₯Ό JSON β RDD ννλ‘ λ³ν -> λ€λμ λ°μ΄ν°λ₯Ό ν¨κ³Όμ μΌλ‘ μ²λ¦¬κ°λ₯)
7. Sparkμ mysql μ°κ²°
8. MySQLμ λ°μ΄ν° μ μ₯
9. MySQLμ μλ λ°μ΄ν°λ€μ νμ©ν΄ μ€νν¬ SQLμμ λ€μν ν΅κ³μ²λ¦¬
10. Djangoλ₯Ό ν΅ν΄ μΉνμ΄μ§ μμ±

## 4. νμΌ λͺ©λ‘
Youtube APIλ₯Ό ν΅ν΄ μμ λ°μ΄ν°λ₯Ό λΆλ¬μ€κ³  μ μ²λ¦¬ μ§ν & μ μ²λ¦¬μμ μ»μ λ°μ΄ν°λ‘ Kakao APIλ₯Ό μ¬μ©νμ¬ μ₯μ κ²μ => κ° μμμ λμ€λ μ₯μ λ°μ΄ν°λ€ μΆμΆ
+ client-secret.json : GCPμμ λ°κΈν Oauth2 μ¬μ©μ μΈμ¦ μ λ³΄ jsonνμΌ
+ collecting_data.py : Youtube APIλ₯Ό ν΅ν΄ μμ λ°μ΄ν° μΆμΆ
+ consumer.py : μΉ΄νμΉ΄ μ»¨μλ¨Έ
+ data_processing.py : Youtube APIλ₯Ό ν΅ν΄ λΆλ¬μ¨ μμ λ°μ΄ν°λ‘ μ μ²λ¦¬ μ§ν & μ μ²λ¦¬μμ μ»μ λ°μ΄ν°λ‘ Kakao APIλ₯Ό μ¬μ©νμ¬ μ₯μ κ²μ => κ° μμμ λμ€λ μ₯μ λ°μ΄ν°λ€ μΆμΆ
+ google_apis.py : Youtube APIμ search:listμ video:list API μ°κ²°μ½λ
+ manage.py : Django νλ‘μ νΈ μμ
+ producer.py : μΉ΄νμΉ΄ νλ‘λμ
+ rds_create_table.py : AWS RDSμ DBμ μ°κ²° ν νμ΄λΈ μμ±νλ μ½λ
+ rds_insert_data.py : AWS RDS DBμ νμ΄λΈμ λ°μ΄ν° μ½μνλ μ½λ
+ requirements.txt
+ spark-convert-df.py : λ°μ΄ν° ννλ₯Ό Spark DataframeμΌλ‘ λ³ννμ¬ μ§ν(μ¬μ©μ μ μ ν¨μ, casting λ±μ νμ©νμ¬ μνλ ννμ λ°μ΄ν° μμ§)
+ youplace ν΄λ : Django νλ‘μ νΈ ν΄λ


## 5. νμ μκ°
BOAZ DATA ENGINEERING 16TH
* κ³ μμ
* λ₯μ ν
* μ‘κ²½λ―Ό

## 6. μΆκ° μ λ³΄
* notion: https://prickle-ragdoll-392.notion.site/BOAZ-ONLINE-CONFERENCE-2022-c4803bfc11db4bc58e2ad0f1903163fb
* youtube: https://www.youtube.com/watch?v=hHTqEfhHZIs (5:01:00 ~ 5:25:30)  
* web: μΆν λ°°ν¬ μμ 

