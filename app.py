import streamlit as st

st.title("我的第一个 Streamlit 应用 🎈")
st.write("Hello, World! 这是一个用 Python 写的网页应用。")

name = st.text_input("请输入你的名字")
if name:
    st.success(f"你好，{name}！欢迎使用 Streamlit！")

# 显示一个简单的图表
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(df)