# 필요한 라이브러리 가져오기
import streamlit as st 
import plotly.graph_objects as go  
import matplotlib.pyplot as plt  
import common  
import matplotlib.font_manager as fm  # Matplotlib의 폰트 관리자 모듈, 한글 폰트 적용

# common 파일을 통해 웹 페이지 탭 꾸미기
common.page_config() 

# 한글 폰트 설정
font_path = './NanumGothic.ttf'  # 한글 폰트 파일 경로
fontprop = fm.FontProperties(fname=font_path)  # 한글 폰트를 지정한 FontProperties 객체 생성
plt.rc('font', family=fontprop.get_name())  # Matplotlib의 폰트 설정을 한글 폰트로 지정


# common 파일을 통해 데이터프레임 불러오기
df = common.get_data()  

st.title("시도별 의료센터 수") 
st.markdown("- 각 시도에 존재하는 의료센터들의 수를 합쳐서 시도별로 얼마나 많은 수가 존재하는 지 확인")
# 시도별 의료기관 수 계산
# 데이터프레임에서 '시군명' 열을 기준으로 갯수를 계산하여 시도별 의료기관 수 구함
hospital_count = df['시군명'].value_counts()


# 경고 메시지를 표시하지 않도록 설정
st.set_option('deprecation.showPyplotGlobalUse', False)  


tab1, tab2 = st.tabs(["Plotly", "Pyplot"]) 

# Plotly로 바차트 만들기
with tab1:
    fig = go.Figure(data=[go.Bar(x=hospital_count.index, y=hospital_count.values)])  # Plotly의 Figure 객체 생성
    fig.update_layout(
        xaxis=dict(
            title='시도',  # x축 제목 설정
            tickangle=90,  # x축 눈금 레이블 회전 각도 설정
        ),
        yaxis=dict(
            title='의료기관 수',  # y축 제목 설정
        ),
        # title='시도별 의료기관 수',  # 그래프 제목 설정
    )
    st.plotly_chart(fig, use_container_width=True)  # Plotly 그래프를 Streamlit에 표시


# pyplot으로 바차트 만들기
with tab2:
    plt.bar(hospital_count.index, hospital_count.values)  # 막대 그래프 생성
    plt.xlabel('시도', fontproperties=fontprop)  # x축 레이블 설정 (한글 폰트 적용)
    plt.ylabel('의료기관 수', fontproperties=fontprop)  # y축 레이블 설정 (한글 폰트 적용)
    # plt.title('시도별 의료기관 수', fontproperties=fontprop)  # 그래프 제목 설정 (한글 폰트 적용)
    plt.xticks(rotation=90, fontproperties=fontprop)  # x축 눈금 레이블 회전 및 한글 폰트 설정
    st.pyplot()  # Matplotlib 그래프를 Streamlit에 표시
