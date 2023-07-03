import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
#한글 폰트 적용
import matplotlib.font_manager as fm
import common

common.page_config()

# 파일 불러오기
df = common.get_data()

st.title("의료센터별 소재지 및 업무구분")
st.markdown("- 의료센터별 소재지 및 업무구분 : 소재지별 보유 응급의료센터 구분 및 수량 확인")

# 한글 폰트 설정
font_path = './NanumGothic.ttf'  # 한글 폰트 파일 경로
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())


# 소재지도로명주소 문자열 분리
df['소재지도로명주소'].str.split(" ")

# 소재지도로명주소 시,군 단위 문자 추출
df['소재지'] = df['소재지도로명주소'].str.split(" ", expand=True)[1]
df.head(3)

# 소재지별 의료기관 업무구분 분류
df_center = df.copy()
df_center = df_center.groupby(['소재지', '업무구분명']).count()
df_center = df_center.pivot_table(index=['소재지', '업무구분명'], values=['병원명/센터명'])
df_center = df_center.iloc[:, :1]

# 인덱스 재설정
df_center.reset_index()

tab1, tab2 = st.tabs(["Plotly", "Pyplot"]) 

with tab1 :
    # 소재지별 의료기관 업무구분 bar차트
    fig = px.bar(df_center.reset_index(), x='소재지', y='병원명/센터명', color='업무구분명')
    fig.update_layout(
        # title='의료기관별 소재지 및 업무구분',
        font=dict(color='black')
    )
    colors = ['red', 'blue', 'green', 'purple']
    for i, bar in enumerate(fig.data):
        bar.marker.color = colors[i % len(colors)]

    st.plotly_chart(fig)

with tab2:
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_center.reset_index(), x='소재지', y='병원명/센터명', hue='업무구분명' )
    # plt.title('의료기관별 소재지 및 업무구분')
    plt.xlabel('소재지',fontproperties = fontprop)
    plt.ylabel('병원명/센터명',fontproperties = fontprop)
    plt.legend(prop = fontprop)
    plt.xticks(fontproperties=fontprop, rotation=90)
    st.pyplot()