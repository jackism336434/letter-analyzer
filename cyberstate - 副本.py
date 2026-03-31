import streamlit as st
import string
from collections import Counter
import plotly.express as px


def letter_frequency(text):
    text = text.lower()
    filtered_text = [c for c in text if c in string.ascii_lowercase]

    total = len(filtered_text)
    counter = Counter(filtered_text)

    data = []
    for letter in string.ascii_lowercase:
        count = counter.get(letter, 0)
        freq = count / total if total > 0 else 0
        data.append({
            "Letter": letter,
            "Count": count,
            "Frequency": freq
        })

    return data


# 页面配置
st.set_page_config(page_title="Letter Frequency Analyzer", layout="wide")

st.title("🧠 Letter Frequency Analyzer")
st.write("统计英文文本中 26 个字母的频率，并可视化展示")

# ======================
# 左右布局
# ======================
col1, col2 = st.columns([1, 2])

# ======================
# 左侧输入
# ======================
with col1:
    with st.container():
        st.subheader("📥 输入区域")
        st.markdown("---")

        option = st.radio("选择输入方式：", ["输入文本", "上传 .txt 文件"])

        text = ""

        if option == "输入文本":
            text = st.text_area("请输入英文文本：", height=200)

        elif option == "上传 .txt 文件":
            uploaded_file = st.file_uploader("上传 txt 文件", type=["txt"])
            if uploaded_file is not None:
                text = uploaded_file.read().decode("utf-8")

        analyze = st.button("🚀 Analyze")

# ======================
# 右侧结果
# ======================



# ======================
# 初始化 session_state
# ======================
if "data_sorted" not in st.session_state:
    st.session_state.data_sorted = None


with col2:
    with st.container():
        st.subheader("📊 分析结果")
        st.markdown("---")

        st.info("ℹ️ 支持英文文本或 .txt 文件上传")

        # ======================
        # 点击 Analyze → 只负责计算
        # ======================
        if analyze:
            if not text.strip():
                st.warning("⚠️ 请输入文本或上传文件")
            else:
                with st.spinner("🔍 正在分析文本..."):
                    data = letter_frequency(text)
                    st.session_state.data_sorted = sorted(
                        data, key=lambda x: x["Frequency"], reverse=True
                    )

        # ======================
        # 展示结果（关键变化🔥）
        # ======================
        if st.session_state.data_sorted is not None:
            data_sorted = st.session_state.data_sorted

            st.success("✅ 分析完成！")

            # ======================
            # 📊 统计指标
            # ======================
            total_letters = sum(d["Count"] for d in data_sorted)
            top_letter = data_sorted[0]["Letter"]
            top_freq = data_sorted[0]["Frequency"]
            bottom_letter = data_sorted[-1]["Letter"]
            bottom_freq = data_sorted[-1]["Frequency"]

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric("总字母数", total_letters)
            with m2:
                st.metric("最高频字母", f"{top_letter} ({top_freq:.2%})")
            with m3:
                st.metric("最低频字母", f"{bottom_letter} ({bottom_freq:.2%})")

            # ======================
            # 🎚️ Top-N（不会重置🔥）
            # ======================
            top_n = st.slider("🎯 选择高亮 Top N", 1, 10, 5)

            # 标记 Top N
            for i, d in enumerate(data_sorted):
                d["Group"] = "Top" if i < top_n else "Others"

            # 提示
            top_letters = [d["Letter"] for d in data_sorted[:top_n]]
            st.info(f"🔥 Top {top_n} 字母: {top_letters}")

            # ======================
            # 📊 图表
            # ======================
            st.subheader("📊 字母频率柱状图")

            fig = px.bar(
                data_sorted,
                x="Letter",
                y="Frequency",
                color="Group",
                text=[f"{d['Frequency']:.2%}" for d in data_sorted],
                color_discrete_map={
                    "Top": "red",
                    "Others": "lightgray"
                },
                labels={"Frequency": "频率", "Letter": "字母"}
            )

            fig.update_traces(textposition='outside')

            fig.update_layout(
                xaxis_title="字母",
                yaxis_title="频率",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # ======================
            # 📋 折叠表格
            # ======================
            with st.expander("📋 查看详细数据"):
                st.dataframe(data_sorted)
