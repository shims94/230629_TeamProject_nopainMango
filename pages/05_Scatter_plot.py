import streamlit as st 
import matplotlib.pyplot as plt  # Matplotlib: 데이터 시각화를 위한 라이브러리
import plotly.graph_objects as go  # Plotly: 인터랙티브 시각화를 위한 라이브러리
import common  
import matplotlib.font_manager as fm  # 한글 폰트 적용을 위한 라이브러리 가져오기

# common 파일에서 정의된 웹 페이지 탭 꾸미기 함수 호출
common.page_config() 

st.title("소재지 위도와 경도를 이용한")
st.title("의료센터 산점도")

st.markdown("- 각 위치에 얼마나 많은 의료센터들이 몰려 있고, 퍼져 있는 지 확인")
# 한글 폰트 설정
font_path = './NanumGothic.ttf'  # 한글 폰트 파일 경로
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())  # 한글 폰트 설정

# common 파일에서 정의된 데이터프레임을 가져오는 함수 호출
df = common.get_data()  


# 경고 메시지 미출력을 위한 설정
st.set_option('deprecation.showPyplotGlobalUse', False)  


tab1, tab2 = st.tabs(["Plotly", "Pyplot"])  
# Plotly로 산점도 그래프 만들기
with tab1:
    fig = go.Figure(data=[go.Scatter(x=df['경도'], y=df['위도'], mode='markers')])  # Scatter 객체를 사용하여 산점도 그래프 생성
    fig.update_layout(
        xaxis=dict(
            title='경도',
            tickangle=90,
        ),
        yaxis=dict(
            title='위도',
        ),
        # title='소재지 위도와 경도를 이용한 산점도',
    )
    st.plotly_chart(fig, use_container_width=True)  # Plotly 그래프를 Streamlit에 표시


# Pyplot으로 산점도 그래프 만들기
with tab2:
    plt.scatter(df['경도'], df['위도'])  # scatter 함수를 사용하여 산점도 그래프 생성
    plt.xlabel('경도', fontproperties=fontprop)  # x축 레이블 설정 (한글 폰트 적용)
    plt.ylabel('위도', fontproperties=fontprop)  # y축 레이블 설정 (한글 폰트 적용)
    # plt.title('소재지 위도와 경도를 이용한 산점도', fontproperties=fontprop)  # 그래프 제목 설정 (한글 폰트 적용)
    plt.xticks(rotation=90, fontproperties=fontprop)  # x축 눈금 레이블 회전 및 한글 폰트 설정
    st.pyplot()  