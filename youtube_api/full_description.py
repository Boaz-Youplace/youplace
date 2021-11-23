import os
from pprint import pprint
from Google import Create_Service
        
CLIENT_SECRET_FILE = 'client-secret.json' # Oauth2 사용자 인증 정보 json파일 가져오기
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) # description까지 긁어오는 함수 호출


part_string = 'contentDetails,statistics,snippet' # part_string 지정
video_ids = 'CijYBg8tWXs' # video_id로 가져올 수 있음

''' 우려되는 점
이렇게 비디오 id 하나씩 가져오면 금방 cost가 찰 것 같음...
'''

response = service.videos().list(
	part=part_string,
	id=video_ids
).execute()


pprint(response)