from pprint import pprint
from collecting_data import collect_data
import pandas as pd
import re
import time

def data_processing_(data):
    start=time.time()
    
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

    df = pd.DataFrame(id,columns=['id'])
    df['title'] = title
    df['description']= description
    df['publishTime'] = publishTime
    df['likeCount'] = likeCount
    df['viewCount'] = viewCount
    df_new = df.drop(['title','description'],axis=1)
    first_info = df_new.to_dict('record')

    # ***************TITLE***************** #
    

    # 새로운 리스트
    clear_titles = []
    # 텍스트를 가지고 있는 리스트
    for i in df['title']:
        # 영어,숫자 및 공백 제거
        text = re.sub('[^0-9가-힣]',' ',i).strip() #text = re.sub('[^a-zA-Z0-9가-힣]',' ',i).strip()
        clear_titles.append(text)

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
            info.append([searching,places['documents']])
        info_list.append(info)

    #검색결과 없어서 len=0인 것들 제거
    new_info_list2 = []
    for i in range (len(info_list)):
        new_info_list = []
        for j in range (len(info_list[i])):
            if len(info_list[i][j][1]) != 0:
                new_info_list.append([info_list[i][j][0], info_list[i][j][1]])
        new_info_list2.append(new_info_list)

    # 주소가 '제주특별자치도'가 아닌 데이터 삭제해서 [장소이름, [장소검색결과 리스트] 형태로 저장
    real_jeju_info = []
    for i in range (len(new_info_list2)):
        jeju_info = []
        for j in range (len(new_info_list2[i])):
            jeju_json = []
            for k in range (len(new_info_list2[i][j][1])):
                if ((new_info_list2[i][j][1][k]['address_name'].split())[0] == '제주특별자치도') and (new_info_list2[i][j][0].isdigit() ==False):
                    jeju_json.append(new_info_list2[i][j][1][k]) #jeju_json = 제대로된 장소 정보들이 담긴 리스트
            jeju_info.append([new_info_list2[i][j][0], jeju_json]) #jeju_info = [장소이름, [장소검색결과 리스트]]
        real_jeju_info.append(jeju_info)

    # 장소 검색 결과 여러개 인것 맨 앞에 1개만 남기고 삭제
    for i in range (len(real_jeju_info)):
        for j in range (len(real_jeju_info[i])):
            if (len(real_jeju_info[i][j][1]) > 0) :
                real_jeju_info[i][j][1] = real_jeju_info[i][j][1][0]

    # 빈 리스트 제거
    total_place_list = []
    for i in range (len(real_jeju_info)):
        place_list = []
        for j in range (len(real_jeju_info[i])):    
            if len(real_jeju_info[i][j][1]) != 0:
                place_list.append(real_jeju_info[i][j])
        total_place_list.append(place_list)

    # category_name : 여행, 음식점, (문화,예술), (가정,생활=소품샵), 스포츠,레저 인 것들만 추리기!
    total_catergorize_list = []
    for i in range (len(total_place_list)):
        catergorize_list = []
        for j in range (len(total_place_list[i])):
            #여행, 음식점, (문화,예술), (가정,생활=소품샵)
            if ((total_place_list[i][j][1]['category_name'].split())[0] == '여행') or ((total_place_list[i][j][1]['category_name'].split())[0] == '음식점') or ((total_place_list[i][j][1]['category_name'].split())[0] == '문화,예술') or ((total_place_list[i][j][1]['category_name'].split())[0] == '가정,생활') or ((total_place_list[i][j][1]['category_name'].split())[0] == '스포츠,레저') :
                catergorize_list.append(total_place_list[i][j])
        total_catergorize_list.append(catergorize_list)


    # 필요한 정보들만 추려서 새 리스트에 넣기
    total_final_info = []
    li = []
    for i in range (len(total_catergorize_list)):
        semi_final_info = []
        for j in range (len(total_catergorize_list[i])):
            # print(total_place_list[i][j][1]['place_name'])
            final_info = []
            final_info.append(i)
            final_info.append({'place_name':[total_catergorize_list[i][j][1]['place_name']],'x':[total_catergorize_list[i][j][1]['x']], 'y':[total_catergorize_list[i][j][1]['y']]})
            semi_final_info.append(final_info)
            li.append(final_info)
        total_final_info.append(semi_final_info)

    # 장소 정보랑 영상 정보 합치기!!!
    for i in range (len(li)):
        for j in range (len(first_info)):
            if (j == li[i][0]):
                li[i][1].update(first_info[j]) # update : 딕셔너리 두개 합치기

    # ***************DESCRIPTION***************** #
    # 새로운 리스트
    clear_des = []
    # 텍스트를 가지고 있는 리스트
    for i in df['description']:
        # 영어,숫자 및 공백 제거
        text = re.sub('[^0-9가-힣]',' ',i).strip() #text = re.sub('[^a-zA-Z0-9가-힣]',' ',i).strip()
        clear_des.append(text)

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
                if ((new_info_list2_des[i][j][1][k]['address_name'].split())[0] == '제주특별자치도') and (new_info_list2_des[i][j][0].isdigit() ==False):
                    jeju_json_des.append(new_info_list2_des[i][j][1][k]) #jeju_json = 제대로된 장소 정보들이 담긴 리스트
            jeju_info_des.append([new_info_list2_des[i][j][0], jeju_json_des]) #jeju_info = [장소이름, [장소검색결과 리스트]]
        real_jeju_info_des.append(jeju_info_des)

    # 장소 검색 결과가 여러개 인것 -> 맨 앞에 1개만 남기고 삭제
    for i in range (len(real_jeju_info_des)):
        for j in range (len(real_jeju_info_des[i])):
            if (len(real_jeju_info_des[i][j][1]) > 0) :
                real_jeju_info_des[i][j][1] = real_jeju_info_des[i][j][1][0]

    # 빈 리스트 제거
    total_place_list_des = []
    for i in range (len(real_jeju_info_des)):
        place_list_des = []
        for j in range (len(real_jeju_info_des[i])):
            if len(real_jeju_info_des[i][j][1]) != 0:
                place_list_des.append(real_jeju_info_des[i][j])
    total_place_list_des.append(place_list_des)

    # category_name : 여행, 음식점, (문화,예술), (가정,생활=소품샵) 인 것들만 추리기!
    total_catergorize_list_des = []
    for i in range (len(total_place_list_des)):
        catergorize_list_des = []
        for j in range (len(total_place_list_des[i])):
    #여행, 음식점, (문화,예술), (가정,생활=소품샵), 스포츠,레저
            if ((total_place_list_des[i][j][1]['category_name'].split())[0] == '여행') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '음식점') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '문화,예술') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '가정,생활') or ((total_place_list_des[i][j][1]['category_name'].split())[0] == '스포츠,레저') :
                catergorize_list_des.append(total_place_list_des[i][j])
        total_catergorize_list_des.append(catergorize_list_des)


    # 필요한 정보들만 추려서 새 리스트에 넣기
    total_final_info_des = []
    li_des = []
    for i in range (len(total_catergorize_list_des)):
        semi_final_info_des = []
        for j in range (len(total_catergorize_list_des[i])):
            
            final_info_des = []
            final_info_des.append(i)
            final_info_des.append({'place_name':[total_catergorize_list_des[i][j][1]['place_name']],'x':[total_catergorize_list_des[i][j][1]['x']], 'y':[total_catergorize_list_des[i][j][1]['y']]})
            semi_final_info_des.append(final_info_des)
            li_des.append(final_info_des)
        total_final_info_des.append(semi_final_info_des)

    # 장소정보랑 영상 정보 합치기!!!
    for i in range (len(li_des)):
        for j in range (len(first_info)):
            if (j == li_des[i][0]):
                li_des[i][1].update(first_info[j])

    # ***************title 데이터랑 description 데이터 합치기!***************** #

    full_data = []
    for i in li:
        full_data.append(i)
    for j in li_des:
        full_data.append(j)
    

    # 인덱스 제거
    real = []
    for i in range (len(full_data)):
        real.append(full_data[i][1:][0])

    # 중복 제거!!!
    x = list({i['place_name'][0]:i for i in real}.values())
    print("최종 데이터!!!!!")
    pprint(x)
    print("걸린시간 :",time.time()-start)
    return x

    # print(len(x))

# if __name__ =='__main__':
#     q='Jeju vlog'
#     order='rating'
#     max_result=5
#     data = collect_data(q,order)
#     data_processing_(data)