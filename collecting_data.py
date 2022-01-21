from google_apis import create_service
from pprint import pprint

        
def collect_data(q,order,publishedAfter=None,publishedBefore=None):
	CLIENT_SECRET_FILE = 'client-secret.json' # Oauth2 사용자 인증 정보 json파일 가져오기
	API_NAME = 'youtube'
	API_VERSION = 'v3'
	SCOPES = ['https://www.googleapis.com/auth/youtube']
	service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 

	max_result = 10 #임의 설정
	search_response = service.search().list(
		part = 'snippet',
		q = q,
		order = order,
		publishedAfter = publishedAfter,
  		publishedBefore = publishedBefore,
		maxResults = max_result
	).execute()

	# 결과확인
	# pprint(search_response)
	

	video_list=[]
	for n in range(max_result):
		# pprint(search_response['items'][n]['id']['videoId'])
		video_id = search_response['items'][n]['id']['videoId']
		video_list.append(video_id)
		

	video_response = service.videos().list(
		part='contentDetails,statistics,snippet',
		id=video_list
	).execute()

	# 결과확인
	# pprint(video_response)
	return video_response



# # collect_data('제주 vlog')
# q='Jeju vlog'
# order='rating'
# max_result=5
# publishedAfter = None
# publishedBefore = None
# dataset = collect_data(q,order)
# # records = data_processing_(dataset)
# # pprint(dataset)