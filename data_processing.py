# 실제 실행시키는 파일 & 데이터 전처리

from pprint import pprint
from collecting_data import collect_data
import pandas as pd

q='Jeju vlog'
order='rating'


dataset = collect_data(q,order)
# pprint(collect_data(q,order))

#dataset 가지고 데이터 전처리 쭈욱 진행하면 될 것 같아융 (❁´◡`❁) !
print('************************************************')
data = collect_data(q,order)
# for i in rang?e(len(data['items'])):
    # print(data['items'][i]['id'])
    # print(data['items'][i]['snippet']['description'])

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
print('정제되지 않은 첫 데이터','\n',first_info)

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
print('최종 명사','\n',nouns)

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

  list_jeju_info = []
real_jeju_info = []
for i in range (len(new_info_list2)):
  jeju_info = []
  for j in range (len(new_info_list2[i])):
    jeju_json = []
    for k in range (len(new_info_list2[i][j][1])):
      #if len(new_info_list2[i][j])>0:
        #print((new_info_list2[i][j][1][k]['address_name'].split())[0])
      if (new_info_list2[i][j][1][k]['address_name'].split())[0] == '제주특별자치도':
        #if (new_info_list2[i][j][0] == new_info_list2[i][j][1][k]['place_name']):
          jeju_json.append(new_info_list2[i][j][1][k]) #jeju_json = 제대로된 장소 정보들이 담긴 리스트
          #print(info[i][1][j])
    jeju_info.append([new_info_list2[i][j][0], jeju_json]) #jeju_info = [장소이름, [장소검색결과 리스트]]
  real_jeju_info.append(jeju_info)
print('1. 주소지가 제주도인 데이터들만 놔두기','\n', real_jeju_info)

# 장소 검색 결과 여러개 인것 맨 앞에 1개만 남기고 삭제
for i in range (len(real_jeju_info)):
  for j in range (len(real_jeju_info[i])):
    if (len(real_jeju_info[i][j][1]) > 0) :
      real_jeju_info[i][j][1] = real_jeju_info[i][j][1][0]
print('2. 장소 검색결과 1개만 놔두기','\n',real_jeju_info)

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
print('3. 빈 리스트 제거 : ', total_place_list)
# print(len(total_place_list))

# 필요한 정보들만 추려서 새 리스트에 넣기
total_final_info = []
li = []
for i in range (len(total_place_list)):
  semi_final_info = []
  for j in range (len(total_place_list[i])):
    # print(total_place_list[i][j][1]['place_name'])
    final_info = []
    final_info.append(i)
    final_info.append({'place_name':[total_place_list[i][j][1]['place_name']]})
    final_info.append({'x':[total_place_list[i][j][1]['x']]})
    final_info.append({'y':[total_place_list[i][j][1]['y']]})
    semi_final_info.append(final_info)
    li.append(final_info)
    # print(final_info)
  # my_set = set(semi_final_info)
  # semi_final_info = list(my_set)
  # print(semi_final_info)
  total_final_info.append(semi_final_info)
# print(total_final_info)
# print("final:::::", li)

# 장소 정보랑 영상 정보 합치기!!!
for i in range (len(li)):
  for j in range (len(first_info)):
    if (j == li[i][0]):
      li[i].append(first_info[j])
print('4. 정리된 정보들')
for i in li:
  print(i)
