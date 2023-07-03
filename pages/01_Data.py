import streamlit as st
import common

common.page_config()
st.title("사용될 데이터")
st.dataframe(common.get_data(),
             use_container_width=True,
             hide_index=True)