from tokenize import Double
import pymysql
import mysql.connector

# create DB
mydb = mysql.connector.connect(
    host = "localhost",
    user = "skm",
    password = "0000"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE youplace")
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)

# connect DB
db = None

try:
    db = pymysql.connect(host='localhost', user='skm', passwd='0000',db='youplace',charset='utf8')
    print("DB connection success")
    # create Table
    sql = '''
    create table tb_youplace(
        id varchar(32) not null,
        place_name varchar(32) not null,
        viewCount int,
        publishTime varchar(32),
        likeCount int,
        x decimal(24,18),
        y decimal(24,18),
        category varchar(32),
        place_url varchar(32),
        address_6 varchar(32),
        primary key(id,place_name)
        )
        ''' 
        #engine = InnoEB default charset=utf8


    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print("DB connection close success")