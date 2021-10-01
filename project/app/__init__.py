
from flask import Flask

# app = Flask(__name__) # 플라스크 애플리케이션 생성
# # __name__에는 모듈명이 담김 ( 즉, 파일 이름인 pybo라는 문자열이 담김 )

# @app.route('/') # 특정 주소에 접속하면 바로 다음 줄에 있는 함수를 호출하는 플라스크의 데코레이터
# def hello_pybo():
#     return 'Hello,Pybo!'

def create_app():
    app=Flask(__name__)
    
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app
# flask 클래스로 만든 객체인 변수 app을 전역에 두지 않고, 함수로 감쌈