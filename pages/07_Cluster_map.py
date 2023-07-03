import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import common

# 웹 페이지 탭 꾸미기
common.page_config()

st.title("시군별 병원 및 의료센터 군집화 지도")

@st.cache  # 데이터 캐싱을 위한 데코레이터
def load_data():
    data = common.get_data()  # common 파일에서 정의된 데이터를 가져오는 함수 호출
    data['소재지'] = data['소재지도로명주소'].str.split(' ').str[:2].apply(lambda x: ' '.join(x))
    data = data[['시군명', '병원명/센터명', '업무구분명', '대표전화번호', '소재지', '소재지도로명주소', '소재지지번주소', '소재지우편번호', '위도', '경도', '응급의료지원센터여부', '전문응급의료센터여부', '전문응급센터전문분야', '권역외상센터여부', '지역외상센터여부']]
    return data

@st.cache_data(experimental_allow_widgets=True)  # 데이터 캐싱을 위한 데코레이터 (위젯 사용 가능)
def load_map():
    data = load_data()  # 데이터를 가져오는 함수 호출

    m = folium.Map(location=[37.291887, 126.996340], zoom_start=9)  # Folium 지도 객체 생성

    marker_cluster = plugins.MarkerCluster().add_to(m)  # Folium 플러그인을 사용한 군집화 마커 생성

    # 데이터를 순회하며 마커 생성
    for idx, row in data.iterrows():
        popup_text = f"<b>병원/센터명:</b> {row['병원명/센터명']}<br>" \
                    f"<b>대표전화번호:</b> {row['대표전화번호']}"
        if row['응급의료지원센터여부'] == 'Y':
            popup_text += "<br><b>응급의료지원센터여부:</b> Y"
        if row['전문응급의료센터여부'] == 'Y':
            popup_text += "<br><b>전문응급의료센터여부:</b> Y"
        if row['권역외상센터여부'] == 'Y':
            popup_text += "<br><b>권역외상센터여부:</b> Y"
        if row['지역외상센터여부'] == 'Y':
            popup_text += "<br><b>지역외상센터여부:</b> Y"

        # 마커 생성 및 지도에 추가
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(marker_cluster)

    # 시군별 병원/의료센터 수를 계산하여 마커 생성
    hospital_counts = data.groupby('소재지')['병원명/센터명'].count().reset_index()
    for idx, row in hospital_counts.iterrows():
        city = row['소재지']
        count = row['병원명/센터명']
        location = (data.loc[data['소재지'] == city, '위도'].mean(), data.loc[data['소재지'] == city, '경도'].mean())

        # 마커 생성 및 지도에 추가
        folium.Marker(
            location=location,
            icon=folium.DivIcon(
                html=f'<div style="font-weight: bold; color: red; font-size: 14px;">{count}</div>',
                icon_size=(30, 30),
                icon_anchor=(15, 15),
            ),
            tooltip=f'{city}: {count} hospitals/centers',
        ).add_to(m)

    st.write("* 시군별 병원 및 의료센터 숫자와 위치 확인.  \n* 위치 클릭 시, 병원 이름과 대표 번호 및 특수 센터 보유 여부 확인 가능.")

    st_folium(m)  # Folium 지도를 Streamlit에 표시

if __name__ == "__main__":
    load_map()  # 지도 생성 함수 호출