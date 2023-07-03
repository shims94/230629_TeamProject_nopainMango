import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import common

#한글 폰트 적용
import matplotlib.font_manager as fm

common.page_config()

st.title("각종 의료 센터/기관 구분별 분포도")
st.markdown("- 각종 의료 센터/기관 구분별 분포도 : 경기도 내 응급의료센터 구성 비율 확인")

# 한글 폰트 설정
font_path = './NanumGothic.ttf'  # 한글 폰트 파일 경로
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())

df = common.get_data()

# 챗지피한테 물어보기
st.set_option('deprecation.showPyplotGlobalUse', False)

df['소재지도로명주소'].str.split(" ")
df['시군'] = df['소재지도로명주소'].str.split(" ", expand=True)[1]
center_values = df['업무구분명'].value_counts()
labels = center_values.index
counts = center_values.values

tab1, tab2 = st.tabs(["Plotly", "Pyplot"])

# plotly로 파이차트 만들기
with tab1:
    fig = go.Figure(data=go.Pie(
        labels=labels,
        values=counts,
        textinfo='percent',
        hoverinfo='label+percent',
    ))
    fig.update_layout(
        # title='기관구분별 분포',
        font=dict(family=fontprop.get_name()),
    )
    st.plotly_chart(fig, use_container_width=True)


# pyplot으로 파이차트 만들기
with tab2:
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90,textprops={'fontproperties': fontprop} )
    ax.axis('equal')  # 원형 모양 유지
    # ax.set_title('기관구분별 분포', fontproperties=fontprop)
    st.pyplot(fig)
