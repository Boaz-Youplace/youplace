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