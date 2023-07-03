# 필요한 라이브러리 가져오기
import streamlit as st 
from streamlit_folium import st_folium  # Streamlit-Folium: Streamlit에 Folium 지도 표시를 위한 라이브러리
import folium  # Folium: 인터랙티브 지도 생성을 위한 라이브러리
import pandas as pd  
import common 

# common 파일에서 정의된 웹 페이지 탭 꾸미기 함수 호출
common.page_config()  

st.title("기본 지도 공간 시각화")
st.markdown("- 데이터 셋에 포함된 각 의료센터들을 지도에 마커 표시")

# 데이터 캐싱을 위한 데코레이터 설정
@st.cache_data(experimental_allow_widgets=True)  
def load_map():
    # common 파일에서 정의된 데이터프레임을 가져오는 함수 호출
    df = common.get_data() 

    # 서울-경기도 부근 지도 생성
    m = folium.Map(location=[37.291887, 126.996340], zoom_start=9)

    # 데이터프레임 순회하며 위치 표시
    for index, row in df.iterrows():
        if pd.notnull(row['위도']) and pd.notnull(row['경도']):
            lat, lon = row['위도'], row['경도']

            # 서울-경기도 부근인 경우에만 표시
            if 37.0 <= lat <= 38.5 and 126.0 <= lon <= 127.5:
                folium.Marker(location=[lat, lon]).add_to(m)  # Folium의 Marker 객체를 사용하여 위치 표시

    # Streamlit-Folium을 사용하여 Folium 지도를 Streamlit에 표시
    st_folium(m) 

if __name__ == "__main__":
    load_map()  # load_map 함수 호출하여 지도 출력
