import streamlit as st
import pandas as pd

# 데이터를 캐시에 저장하는 함수
@st.cache_data
def get_data():
    return pd.read_csv("./hospital.csv",encoding="cp949")

# 캐싱은 데이터를 로딩하는 시간을 줄여줌.

# 페이지 설정을 위한 함수
def page_config():
    # 페이지 제목과 아이콘 설정
    st.set_page_config(
        page_title="경기 의료기관 데이터 시각화",
        page_icon="🏥",
    )