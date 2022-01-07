import os
from pprint import pprint
from google_apis import create_service
        

CLIENT_SECRET_FILE = 'koeunseo-client-secret.json' # Oauth2 사용자 인증 정보 json파일 가져오기
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']


service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) # description까지 긁어오는 함수 호출

part_string = 'contentDetails,statistics,snippet' # part_string 지정
video_ids = 'zMjZ6z1OOPs' # video_id로 가져올 수 있음
video_list = ['B_7Hr4Z_S64', 'Zsi7UbXk8h4', '4h-359Th53Y', 'RDFnPHi389E', 'd6LQU0evTxA', 'bMuOplKgzHg', 'NU1Xyzql7tk', '-z4PgQNHxfQ', 'MTSb6sMdDOs', 'U4NAYSJ-K3o', 'E-WuKtzYzm8', 'Wf7bcqPyBiA', 'PnBi0YOyM8c', '9xWGdT1cp8E', 'AmHB3P62QPU', 'zMjZ6z1OOPs', '8xEE-_qsSY4', 'EVqx1Zo-jHQ', 'j9BtiZMn8DI', 'n45sTixvy-I', 'V83RUWuclf4', 'PmIdpfoWfZ0', 'bP2NB2ybIxo', '1PDvARQeOFI', 'DjvY9f6OUsM', 'dsE8hj6Lhws', 'A_uqFEWoCJo', 'ACOXj9TiE-s', 'rzfu6XZOiJg', 'TVCi0-g-7Gc', 'a05FmW3Fm0s', 'j3L40NHZcGw', 'fEc_QGyMERI', 'UZvTU7umApI', 'ki8QkFMTRPk', 'vmVUMdxxq4Y', 'PhAElDDoiWA', 'ODkTPbYLZYQ', '-ycWUJy3TPs', '88wnoQ0T2SQ', 'D_ZmbHDw38g', '7jt7s8XC0M4', 'nwUYZhmn24A', 'MzwpzvsXoHA', '4Q8PWIf9gp8', 'tYvXn-LK0zY', '1zuIxRT9pp0', '80FnUG4oq_U', 'M7SbP8TbzSs', 'pnG9CBkuw1Y', '7a7wutuwzDE', 'fnYQa9p_CLU', 'kzK-sMxh9zs', '69Z9kIEqtSY', 'CWXP6fCnS_E', 'VDLSOA5u2JU', '7xSqK7bQgS4', 'fiN5zGP2qEg', '1mpeWpFNGl8', 'gdQzYodMvko', '8-OTwfY8UCE', 'QLwReulBHA4', '9HE4YPn9WRg', 'IA0EU4QA8sI', 'QeoxKw6SUIw', 'vWfvXGq2lTY', 'L0yMexHKCEc', 'Y_8s5hsWJxM', '9TrHW8zZd7M', 'd-xRbUJucdM', 'rpl7XoJUW0I', 'k_TQDu-dZ_4', 'DXvzaA9oUpY', 'x1KRX_l-BbE', 'w_0kA1JulHE', 'sqDPFECnEtk', 'm2Ck2Xlurz8', 'AsD5KrifizE', 'rFY-aVFWGmg', 'EzdedbJWeK0', 'kn_dx1czwnM', '3Xdx5Ti9Sik', 'MAuWrkRPnGI', 'czsx9narzh8', 'ldl14v0HjO4', 'GjmPKUBW7Zg', '_fdhnnKsW2Q', 'cpRd_roSIwY', 'OdExxH6xPQ0', 'IGPHZTFtzPw', 'Q-dkFwV2SXM', '3VIrsxBG1gA', '8FHhGICs7MA', 'oEyIBkwK3AA', '-VBZSKXREhQ', 'DNc9lidSR5I', 'L5o1cynzUxw', 'XOgm-XEyGbM', 'biy7_ZY6k5Q', 'KMeeUgJ6v1E']
video_list=video_list[:10]

for video in video_list:
	response = service.videos().list(
		part=part_string,
		id=video
	).execute()

	pprint(response)