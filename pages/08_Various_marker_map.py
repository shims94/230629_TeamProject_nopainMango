import streamlit as st
from streamlit_folium import st_folium, folium_static
import folium
import common

# 응급센터 종류
eCenter_array = ("응급의료지원센터여부", "전문응급의료센터여부", "전문응급센터전문분야", "권역외상센터여부", "지역외상센터여부")

# 응급센터가 존재하는지 체크하는 함수
def check_option(row) :
    if row[eCenter_array[0]] == 'Y': return '<b>응급의료지원센터</b>'
    elif row[eCenter_array[1]] == 'Y': return '<b>전문응급의료센터</b>'
    elif row[eCenter_array[2]] == 'Y': return '<b>전문응급센터전문분야</b>'
    elif row[eCenter_array[3]] == 'Y': return '<b>권역외상센터</b>'
    elif row[eCenter_array[4]] == 'Y': return '<b>지역외상센터</b>'

# 초기맵 생성
def create_map():
    m = folium.Map(location=[37.291887, 126.996340], zoom_start=9)
    return m

def add_marker(map_obj, df):
    # 업무 구분명이 지역센터나 기관일경우 녹색 하트마커, 그이외(광역) 빨강 스타마커
    for index, row in df.iterrows():
        if row['업무구분명'] == '지역센터' or row['업무구분명'] == '지역기관':
            folium.Marker(location=[row['위도'], row['경도']],
                          popup=folium.Popup(f"{row['병원명/센터명']}<br>", max_width=300),
                          icon=folium.Icon(color='green', icon='heart')
                          ).add_to(map_obj)
        # 지역급이아니면(광역급)
        else:
            folium.Marker(location=[row['위도'], row['경도']],
                          popup=folium.Popup(f"{row['병원명/센터명']}<br>", max_width=300),
                          icon=folium.Icon(color='yellow', icon='star')
                          ).add_to(map_obj)
# 특정 응급센터만 표시하는 마커추가
def add_special_marker(map_obj, df):
    for index, row in df.iterrows():
        for i in range(len(eCenter_array)):
            if row[eCenter_array[i]] == 'Y':
                 folium.Marker(location=[row['위도'], row['경도']],
                               popup=folium.Popup(f"{row['병원명/센터명']}<br>", max_width=300),
                               tooltip=row[eCenter_array[i]],
                               icon=folium.Icon(color='orange', icon='heart')
                               ).add_to(map_obj)
def main():
    common.page_config()
    st.title("의료시설 마커 표시 지도")
    st.markdown("**지역급 의료시설 :** 초록색하트마커   /   **권역급 의료시설 :** 빨간색별마커")
    # 초기 지도
    initial_map = create_map()
    map_obj = None
    # 데이터 불러옴
    df = common.get_data()
    map_obj = create_map()
    add_marker(map_obj,df)
    # 버튼을 가로열에 배치하기위해 컬럼을 나눔(버튼갯수만큼)
    col1, col2, col3 = st.columns(3)
    with col1:
        # 클릭하면 지도상의 마커를 모두 지우고 표시
        if st.button('**마커지우기**'):
            map_obj = initial_map
    with col2:
        # 클릭하면 모든 병원표시
        if st.button('**모든 병원표시**'):
            add_marker(map_obj, df)
    with col3:
        # 클릭하면 지도상의 마커를 지우고 응급시설 표시
        if st.button('**응급의료지원센터**'):
            map_obj = initial_map
            add_special_marker(map_obj, df)
    if map_obj is not None:
        folium_static(map_obj)
    else:
        folium_static(initial_map)

if __name__ == "__main__":
    main()