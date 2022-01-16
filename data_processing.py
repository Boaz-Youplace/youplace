# 실제 실행시키는 파일 & 데이터 전처리

from pprint import pprint
from collecting_data import collect_data

import pandas as pd

# q='Jeju vlog'
# order='rating'

# dataset = collect_data(q,order)
# pprint(collect_data(q,order))
def data_processing_(data):
  id = []
  title = []
  description = []
  publishTime = []
  likeCount = []
  viewCount = []

  for i in range (len(data['items'])):
    id.append(data['items'][i]['id'])
    title.append(data['items'][i]['snippet']['localized']['title'])
    description.append(data['items'][i]['snippet']['localized']['description'])
    publishTime.append(data['items'][i]['snippet']['publishedAt'])
    likeCount.append(data['items'][i]['statistics']['likeCount'])
    viewCount.append(data['items'][i]['statistics']['viewCount'])
    # print('id:', data['items'][i]['id'])
    # print('title:', data['items'][i]['snippet']['localized']['title'])
    # print('description:', data['items'][i]['snippet']['localized']['description'])
    # print('publishedAt:', data['items'][i]['snippet']['publishedAt'])
    # print('likecount:', data['items'][i]['statistics']['likeCount'])
    # print('viewcount:', data['items'][i]['statistics']['viewCount'],'\n')

  df = pd.DataFrame(id,columns=['id'])
  df['title'] = title
  df['description']= description
  df['publishTime'] = publishTime
  df['likeCount'] = likeCount
  df['viewCount'] = viewCount
  df_new = df.drop(['title','description'],axis=1)
  first_info = df_new.to_dict('record')
  # print('정제되지 않은 첫 데이터','\n',first_info)

  # ***************TITLE***************** #
  #!/usr/bin/env python
  import re

  # 새로운 리스트
  clear_titles = []
  # 텍스트를 가지고 있는 리스트
  for i in df['title']:
      # 영어,숫자 및 공백 제거
      text = re.sub('[^0-9가-힣]',' ',i).strip() #text = re.sub('[^a-zA-Z0-9가-힣]',' ',i).strip()
      clear_titles.append(text)
  # print(df['title'])
  # print("##")
  # print(clear_titles)

  nouns = []
  for i in range (len(clear_titles)):
    nouns.append(clear_titles[i].split())
  # print(nouns)

  # '브이로그' 단어 빼기
  for i in range (len(nouns)):
    if "제주도" in nouns[i]:
        nouns[i].remove("제주도")
    if "제주" in nouns[i]:
        nouns[i].remove("제주")
    if "브이로그" in nouns[i]:
        nouns[i].remove("브이로그")
    if "여행" in nouns[i]:
        nouns[i].remove("여행")
    if "제주도여행" in nouns[i]:
        nouns[i].remove("제주도여행")
    if "제주여행" in nouns[i]:
        nouns[i].remove("제주여행")
  # print('최종 명사','\n',nouns)

  #kakao API로 장소검색
  import requests

  info_list = []
  for i in range (len(nouns)):
    info = []
    for j in range (len(nouns[i])):
      searching = nouns[i][j]
      url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
      headers = {
      "Authorization": "KakaoAK de5c6d93b8be1b90b6c34d80949d0d4c"
      }
      places = requests.get(url, headers = headers).json()#['documents']
      # print("장소:",searching, ", json:", places['documents'])
      info.append([searching,places['documents']])
    info_list.append(info)
  # print(info_list)

  #검색결과 없어서 len=0인 것들 제거
  new_info_list2 = []
  for i in range (len(info_list)):
    new_info_list = []
    for j in range (len(info_list[i])):
      if len(info_list[i][j][1]) != 0:
        new_info_list.append([info_list[i][j][0], info_list[i][j][1]])
    new_info_list2.append(new_info_list)

  # 주소가 '제주특별자치도'가 아닌 데이터 삭제해서 [장소이름, [장소검색결과 리스트] 형태로 저장
  list_jeju_info = []
  real_jeju_info = []
  for i in range (len(new_info_list2)):
    jeju_info = []
    for j in range (len(new_info_list2[i])):
      jeju_json = []
      for k in range (len(new_info_list2[i][j][1])):
        #if len(new_info_list2[i][j])>0:
          #print((new_info_list2[i][j][1][k]['address_name'].split())[0])
        if ((new_info_list2[i][j][1][k]['address_name'].split())[0] == '제주특별자치도') and (new_info_list2[i][j][0].isdigit() ==False):
          #if (new_info_list2[i][j][0] == new_info_list2[i][j][1][k]['place_name']):
            jeju_json.append(new_info_list2[i][j][1][k]) #jeju_json = 제대로된 장소 정보들이 담긴 리스트
            #print(info[i][1][j])
      jeju_info.append([new_info_list2[i][j][0], jeju_json]) #jeju_info = [장소이름, [장소검색결과 리스트]]
    real_jeju_info.append(jeju_info)
  # print('1. 주소지가 제주도인 데이터들만 놔두기','\n', real_jeju_info)

  # 장소 검색 결과 여러개 인것 맨 앞에 1개만 남기고 삭제
  for i in range (len(real_jeju_info)):
    for j in range (len(real_jeju_info[i])):
      if (len(real_jeju_info[i][j][1]) > 0) :
        real_jeju_info[i][j][1] = real_jeju_info[i][j][1][0]
  # print('2. 장소 검색결과 1개만 놔두기','\n',real_jeju_info)

  # 빈 리스트 제거
  total_place_list = []
  for i in range (len(real_jeju_info)):
    # print("origin : ",real_jeju_info[i])
    place_list = []
    for j in range (len(real_jeju_info[i])):
      # print(real_jeju_info[i][j])
      if len(real_jeju_info[i][j][1]) != 0:
        place_list.append(real_jeju_info[i][j])
    # print('fix : ', place_list)
    total_place_list.append(place_list)
  # print('3. 빈 리스트 제거 : ', '\n', total_place_list)
  # print(len(total_place_list))

  # category_name : 여행, 음식점, (문화,예술), (가정,생활=소품샵), 스포츠,레저 인 것들만 추리기!
  total_catergorize_list = []
  for i in range (len(total_place_list)):
    catergorize_list = []
    for j in range (len(total_place_list[i])):
      # print(total_place_list[i][j])
      # print(total_place_list[i][j][1]['category_name'])
      # print((total_place_list[i][j][1]['category_name'].split())[0])
      #여행, 음식점, (문화,예술), (가정,생활=소품샵)
      if ((total_place_list[i][j][1]['category_name'].split())[0] == '여행') or ((total_place_list[i][j][1]['category_name'].split())[0] == '음식점') or ((total_place_list[i][j][1]['category_name'].split())[0] == '문화,예술') or ((total_place_list[i][j][1]['category_name'].split())[0] == '가정,생활') or ((total_place_list[i][j][1]['category_name'].split())[0] == '스포츠,레저') :
        catergorize_list.append(total_place_list[i][j])
    total_catergorize_list.append(catergorize_list)
  # len(total_catergorize_list)
  # print(total_catergorize_list)

  # 카테고리 소분류 하기 '관광,명소', '숙박', '여행'(기타라고 보면 될듯?), '문화,예술', '스포츠,레저', ' 가정,생활', '카페' ,'음식점' 으로 분류함
  num = 0
  for i in range (len(total_catergorize_list)):
    num += len(total_catergorize_list[i])
  # print(num)
  category_list = [0 for i in range(num)]

  num2 = 0
  for i in range (len(total_catergorize_list)):
    for j in range (len(total_catergorize_list[i])):
      # print('origin : ',total_catergorize_list[i][j][1]['category_name'].split())
      # # print('origin : ',total_catergorize_list[i][j][1]['category_name'].split()[2])
      # print('num', num2)
      if ('관광,명소' in total_catergorize_list[i][j][1]['category_name'].split()):
        category_list[num2] = '관광,명소'
      elif ('숙박' in (total_catergorize_list[i][j][1]['category_name'].split())):
        category_list[num2] = '숙박'
      elif ('여행' in (total_catergorize_list[i][j][1]['category_name'].split())): #공원
        category_list[num2] = '여행'
      elif ('문화,예술' in (total_catergorize_list[i][j][1]['category_name'].split())):
        category_list[num2] = '문화,예술'
      elif ('스포츠,레저' in (total_catergorize_list[i][j][1]['category_name'].split())):
        category_list[num2] = '스포츠,레저'
      elif ('가정,생활' in (total_catergorize_list[i][j][1]['category_name'].split())):
        category_list[num2] = '가정,생활'
      if ('카페' in (total_catergorize_list[i][j][1]['category_name'].split())) :
        category_list[num2] = '카페'
      elif ('음식점' in (total_catergorize_list[i][j][1]['category_name'].split())):
        category_list[num2] = '음식점'
      num2 +=1
      # print('fix : ',category_list)

  # 주소지를 '제주시내', '애월,한림', '중문', '서귀포', '성산,우도', '조천,구좌' 로 나누기
  # -> '서귀포시(서귀포시 중부)', '안덕,대정(서귀포시 서부)', '남원,표선,성산(서귀포시 동부)', '조천,구좌,우도(제주시 동부)', '애월,한림,한경(제주시 서부)', '제주시내(제주시 중부)'
  a = 0
  for i in range (len(total_catergorize_list)):
    a += len(total_catergorize_list[i])
  # print(a)
  address_list = [0 for i in range(a)]

  num3 = 0
  for i in range (len(total_catergorize_list)):
    for j in range (len(total_catergorize_list[i])):
      # print('origin : ', total_catergorize_list[i][j][1]['address_name'])
      #서귀포시 중부
      if '서귀포시' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '서귀포시(서귀포시 중부)'
      #서귀포시 서부
      elif '대정읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '안덕,대정(서귀포시 서부)'
      elif '안덕면' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '안덕,대정(서귀포시 서부)'
      #서귀포시 동부
      elif '납원읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '남원,표선,성산(서귀포시 동부)'
      elif '표선면' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '남원,표선,성산(서귀포시 동부)'
      elif '성산읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '남원,표선,성산(서귀포시 동부)'
      #제주시 동부
      elif '조천읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '조천,구좌,우도(제주시 동부)'
      elif '구좌읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '조천,구좌,우도(제주시 동부)'
      elif '우도면' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '조천,구좌,우도(제주시 동부)'
      #제주시 서부
      elif '애월읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '애월,한림,한경(제주시 서부)'
      elif '한림읍' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '애월,한림,한경(제주시 서부)'
      elif '한경면' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '애월,한림,한경(제주시 서부)'
      #제주시 중부
      elif '제주시' in total_catergorize_list[i][j][1]['address_name'] :
        address_list[num3] = '제주시내(제주시 중부)'
      num3+=1
      # print('fix : ', address_list)


  # 필요한 정보들만 추려서 새 리스트에 넣기
  total_final_info = []
  li = []
  n = 0
  for i in range (len(total_catergorize_list)):
    semi_final_info = []
    for j in range (len(total_catergorize_list[i])):
      # print(total_place_list[i][j][1]['place_name'])
      final_info = []
      final_info.append(i)
      # final_info.append({'place_name':[total_catergorize_list[i][j][1]['place_name']]})
      # final_info.append({'x':[total_catergorize_list[i][j][1]['x']]})
      # final_info.append({'y':[total_catergorize_list[i][j][1]['y']]})
      final_info.append({'place_name':[total_catergorize_list[i][j][1]['place_name']],'x':[total_catergorize_list[i][j][1]['x']], 'y':[total_catergorize_list[i][j][1]['y']], 'place_url':total_catergorize_list[i][j][1]['place_url'], 'category':category_list[n], 'address_6': address_list[n]})
      semi_final_info.append(final_info)
      li.append(final_info)
      n+=1
      # print(final_info)
    total_final_info.append(semi_final_info)
  # print(total_final_info)
  # print("final:::::", li)

  # 장소 정보랑 영상 정보 합치기!!!
  for i in range (len(li)):
    for j in range (len(first_info)):
      if (j == li[i][0]):
        li[i][1].update(first_info[j]) # update : 딕셔너리 두개 합치기
  # print('4. title 정리된 정보들')
  # print(li)


  # ***************DESCRIPTION***************** #
  #!/usr/bin/env python
  import re

  # 새로운 리스트
  clear_des = []
  # 텍스트를 가지고 있는 리스트
  for i in df['description']:
      # 영어,숫자 및 공백 제거
      text = re.sub('[^0-9가-힣]',' ',i).strip() #text = re.sub('[^a-zA-Z0-9가-힣]',' ',i).strip()
      clear_des.append(text)
  # print(df['description'])
  # print("##")
  # print(clear_des)

  nouns_des = []
  for i in range (len(clear_des)):
    nouns_des.append(clear_des[i].split())
  # print('Description 명사화', '\n', nouns_des)

  # '브이로그' 단어 빼기
  for i in range (len(nouns_des)):
    if "제주도" in nouns_des[i]:
        nouns_des[i].remove("제주도")
    if "제주" in nouns_des[i]:
        nouns_des[i].remove("제주")
    if "브이로그" in nouns_des[i]:
        nouns_des[i].remove("브이로그")
    if "여행" in nouns_des[i]:
        nouns_des[i].remove("여행")
    if "제주도여행" in nouns_des[i]:
        nouns_des[i].remove("제주도여행")
    if "제주여행" in nouns_des[i]:
        nouns_des[i].remove("제주여행")
  # print(nouns_des)

  # 카카오 API
  import requests

  info_list_des = []
  for i in range (len(nouns_des)):
    info_des = []
    for j in range (len(nouns_des[i])):
      searching = nouns_des[i][j]
      url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
      headers = {
      "Authorization": "KakaoAK de5c6d93b8be1b90b6c34d80949d0d4c"
      }
      places = requests.get(url, headers = headers).json()#['documents']
      # print("장소:",searching, ", json:", places['documents'])
      info_des.append([searching,places['documents']])
    info_list_des.append(info_des)

  #검색결과 없어서 len=0인 것들 제거
  new_info_list2_des = []
  for i in range (len(info_list_des)):
    new_info_list_des = []
    for j in range (len(info_list_des[i])):
      if len(info_list_des[i][j][1]) != 0:
        new_info_list_des.append([info_list_des[i][j][0], info_list_des[i][j][1]])
    new_info_list2_des.append(new_info_list_des)

  # 주소가 '제주특별자치도' 아닌 것 삭제
  list_jeju_info_des = []
  real_jeju_info_des = []
  for i in range (len(new_info_list2_des)):
    jeju_info_des = []
    for j in range (len(new_info_list2_des[i])):
      jeju_json_des = []
      for k in range (len(new_info_list2_des[i][j][1])):
        #if len(new_info_list2[i][j])>0:
          #print((new_info_list2[i][j][1][k]['address_name'].split())[0])
        if ((new_info_list2_des[i][j][1][k]['address_name'].split())[0] == '제주특별자치도') and (new_info_list2_des[i][j][0].isdigit() ==False):
          #if (new_info_list2[i][j][0] == new_info_list2[i][j][1][k]['place_name']):
            jeju_json_des.append(new_info_list2_des[i][j][1][k]) #jeju_json = 제대로된 장소 정보들이 담긴 리스트
            #print(info[i][1][j])
      jeju_info_des.append([new_info_list2_des[i][j][0], jeju_json_des]) #jeju_info = [장소이름, [장소검색결과 리스트]]
    real_jeju_info_des.append(jeju_info_des)
  # print(real_jeju_info_des)

  # 장소 검색 결과가 여러개 인것 -> 맨 앞에 1개만 남기고 삭제
  for i in range (len(real_jeju_info_des)):
    for j in range (len(real_jeju_info_des[i])):
      if (len(real_jeju_info_des[i][j][1]) > 0) :
        real_jeju_info_des[i][j][1] = real_jeju_info_des[i][j][1][0]
  # print(real_jeju_info_des)

  # 빈 리스트 제거
  total_place_list_des = []
  for i in range (len(real_jeju_info_des)):
    # print("origin : ",real_jeju_info_des[i])
    place_list_des = []
    for j in range (len(real_jeju_info_des[i])):
      # print(real_jeju_info_des[i][j])
      if len(real_jeju_info_des[i][j][1]) != 0:
        place_list_des.append(real_jeju_info_des[i][j])
    # print('fix : ', place_list_des)
    total_place_list_des.append(place_list_des)
  # print(total_place_list_des)
  # print(len(total_place_list_des))

  # category_name : 여행, 음식점, (문화,예술), (가정,생활=소품샵) 인 것들만 추리기!
  total_catergorize_list_des = []
  for i in range (len(total_place_list_des)):
    catergorize_list_des = []
    for j in range (len(total_place_list_des[i])):
      # print(total_place_list_des[i][j][0])
      # print(total_place_list_des[i][j][1]['category_name'])
      # print((total_place_list_des[i][j][1]['category_name'].split())[0])
      #여행, 음식점, (문화,예술), (가정,생활=소품샵), 스포츠,레저
      if ((total_place_list_des[i][j][1]['category_name'].split())[0] == '여행') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '음식점') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '문화,예술') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '가정,생활') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '스포츠,레저') :
        catergorize_list_des.append(total_place_list_des[i][j])
    total_catergorize_list_des.append(catergorize_list_des)
  # print(len(total_catergorize_list_des))
  # print(total_catergorize_list_des)

  #카테고리 소분류하기 '관광,명소', '숙박', '여행'(기타라고 보면 될듯?), '문화,예술', '스포츠,레저', ' 가정,생활', '카페' ,'음식점' 으로 분류함
  num_des = 0
  for i in range (len(total_catergorize_list_des)):
    num_des += len(total_catergorize_list_des[i])
  # print(num_des)
  category_list_des = [0 for i in range(num_des)]

  num2_des = 0
  for i in range (len(total_catergorize_list_des)):
    for j in range (len(total_catergorize_list_des[i])):
      # print('origin : ',total_catergorize_list_des[i][j][1]['category_name'].split())
      # print('origin : ',total_catergorize_list_des[i][j][1]['category_name'].split()[2])
      # print('num', num2_des)
      if ('관광,명소' in total_catergorize_list_des[i][j][1]['category_name'].split()):
        category_list_des[num2_des] = '관광,명소'
      elif ('숙박' in (total_catergorize_list_des[i][j][1]['category_name'].split())):
        category_list_des[num2_des] = '숙박'
      elif ('여행' in (total_catergorize_list_des[i][j][1]['category_name'].split())): #공원
        category_list_des[num2_des] = '여행'
      elif ('문화,예술' in (total_catergorize_list_des[i][j][1]['category_name'].split())):
        category_list_des[num2_des] = '문화,예술'
      elif ('스포츠,레저' in (total_catergorize_list_des[i][j][1]['category_name'].split())):
        category_list_des[num2_des] = '스포츠,레저'
      elif ('가정,생활' in (total_catergorize_list_des[i][j][1]['category_name'].split())):
        # print('hi')
        category_list_des[num2_des] = '가정,생활'
      if ('카페' in (total_catergorize_list_des[i][j][1]['category_name'].split())) :
        category_list_des[num2_des] = '카페'
      elif ('음식점' in (total_catergorize_list_des[i][j][1]['category_name'].split())):
        category_list_des[num2_des] = '음식점'
      num2_des +=1
      # print('fix : ',category_list_des)

  # 주소지를 '제주시내', '애월,한림', '중문', '서귀포', '성산,우도', '조천,구좌' 로 나누기 -> '서귀포시(서귀포시 중부)', '안덕,대정(서귀포시 서부)', '남원,표선,성산(서귀포시 동부)', '조천,구좌,우도(제주시 동부)', '애월,한림,한경(제주시 서부)', '제주시내(제주시 중부)'
  a_des = 0
  for i in range (len(total_catergorize_list_des)):
    a_des += len(total_catergorize_list_des[i])
  # print(a)
  address_list_des = [0 for i in range(a_des)]

  num3_des = 0
  for i in range (len(total_catergorize_list_des)):
    for j in range (len(total_catergorize_list_des[i])):
      # print('origin : ', total_catergorize_list_des[i][j][1]['address_name'])
      #서귀포시 중부
      if '서귀포시' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '서귀포시(서귀포시 중부)'
      #서귀포시 서부
      elif '대정읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '안덕,대정(서귀포시 서부)'
      elif '안덕면' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '안덕,대정(서귀포시 서부)'
      #서귀포시 동부
      elif '납원읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '남원,표선,성산(서귀포시 동부)'
      elif '표선면' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '남원,표선,성산(서귀포시 동부)'
      elif '성산읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '남원,표선,성산(서귀포시 동부)'
      #제주시 동부
      elif '조천읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '조천,구좌,우도(제주시 동부)'
      elif '구좌읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '조천,구좌,우도(제주시 동부)'
      elif '우도면' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '조천,구좌,우도(제주시 동부)'
      #제주시 서부
      elif '애월읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '애월,한림,한경(제주시 서부)'
      elif '한림읍' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '애월,한림,한경(제주시 서부)'
      elif '한경면' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '애월,한림,한경(제주시 서부)'
      #제주시 중부
      elif '제주시' in total_catergorize_list_des[i][j][1]['address_name'] :
        address_list_des[num3_des] = '제주시내(제주시 중부)'
      num3_des+=1
      # print('fix : ', address_list_des)

  # 필요한 정보들만 추려서 새 리스트에 넣기
  total_final_info_des = []
  li_des = []
  n=0
  for i in range (len(total_catergorize_list_des)):
    semi_final_info_des = []
    for j in range (len(total_catergorize_list_des[i])):
      # print(total_catergorize_list_des[i][j][1]['place_name'])
      final_info_des = []
      final_info_des.append(i)
      # final_info_des.append({'place_name':[total_catergorize_list_des[i][j][1]['place_name']]})
      # final_info_des.append({'x':[total_catergorize_list_des[i][j][1]['x']]})
      # final_info_des.append({'y':[total_catergorize_list_des[i][j][1]['y']]})
      final_info_des.append({'place_name':[total_catergorize_list_des[i][j][1]['place_name']],'x':[total_catergorize_list_des[i][j][1]['x']], 'y':[total_catergorize_list_des[i][j][1]['y']],'place_url':total_catergorize_list_des[i][j][1]['place_url'], 'category':category_list_des[n], 'address_6': address_list_des[n]})
      semi_final_info_des.append(final_info_des)
      li_des.append(final_info_des)
      n+=1
      # print(final_info_des)
    total_final_info_des.append(semi_final_info_des)
  # print(total_final_info_des)
  # print("final:::::", li_des)

  # 장소정보랑 영상 정보 합치기!!!
  for i in range (len(li_des)):
    for j in range (len(first_info)):
      if (j == li_des[i][0]):
        li_des[i][1].update(first_info[j])
  # print('Description 총 정리본 : ')
  # print(li_des)

  # ***************title 데이터랑 description 데이터 합치기!***************** #
  # print(len(li))
  # print(len(li_des))

  full_data = []
  for i in li:
    full_data.append(i)
  for j in li_des:
    full_data.append(j)
  # print(full_data)

  # print(len(full_data))

  # 인덱스 제거
  real = []
  for i in range (len(full_data)):
    # print(full_data[i][1]['place_name'])
    real.append(full_data[i][1:][0])
  # print(real)

  # 중복 제거!!!
  x = list({i['place_name'][0]:i for i in real}.values())
  print("최종 데이터!!!!!")
  pprint(x)
  return x

  # print(len(x))

# q='Jeju vlog'
# order='rating'
# dataset = collect_data(q,order)
# records = data_processing_(dataset)