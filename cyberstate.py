import plotly.express as px
import streamlit as st

from analyzer import (
    SAMPLE_TEXT,
    build_export_csv,
    build_frequency_table,
    build_result_insights,
    build_summary,
)


def render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f6f7f4 0%, #fbfbf9 100%);
            color: #17201f;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        .panel {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid #d8ddd6;
            border-radius: 18px;
            padding: 1.1rem 1.1rem 0.8rem 1.1rem;
            box-shadow: 0 14px 40px rgba(23, 32, 31, 0.06);
        }
        .summary-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin: 0.5rem 0 1rem 0;
        }
        .summary-card {
            background: #f3f5f1;
            border: 1px solid #dbe2da;
            border-radius: 14px;
            padding: 0.85rem 0.95rem;
        }
        .summary-label {
            font-size: 0.82rem;
            color: #5e6c69;
            margin-bottom: 0.2rem;
        }
        .summary-value {
            font-size: 1.25rem;
            font-weight: 600;
            color: #17201f;
        }
        .section-note {
            color: #60706c;
            font-size: 0.93rem;
            margin-top: -0.2rem;
            margin-bottom: 0.8rem;
        }
        .status-box {
            border: 1px dashed #c8d1ca;
            border-radius: 16px;
            padding: 1.2rem 1rem;
            background: rgba(243, 245, 241, 0.8);
            color: #51605d;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(message: str) -> None:
    st.markdown(
        f"""
        <div class="status-box">
            <strong>结果</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="字母频率分析器", layout="wide")
render_styles()

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.title("字母频率分析器")
st.caption("统计英文文本中的字母频率，并提供清晰的可视化结果。")

left_col, right_col = st.columns([1, 1.45], gap="large")

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("输入")
    st.markdown(
        '<div class="section-note">选择输入方式，先查看输入统计，再执行分析。</div>',
        unsafe_allow_html=True,
    )

    input_mode = st.radio(
        "输入方式",
        ("直接输入", "上传 TXT"),
        horizontal=True,
        label_visibility="collapsed",
    )

    input_text = st.session_state.input_text
    if input_mode == "直接输入":
        sample_col, helper_col = st.columns([1, 1.4])
        with sample_col:
            if st.button("填充示例文本", use_container_width=True):
                st.session_state.input_text = SAMPLE_TEXT
                input_text = SAMPLE_TEXT
        with helper_col:
            st.caption("首次使用可以先载入示例文本，了解分析流程后再替换为自己的内容。")

        input_text = st.text_area(
            "英文文本",
            placeholder="请在这里粘贴或输入英文文本……",
            height=260,
            key="input_text",
            label_visibility="collapsed",
        )
    else:
        uploaded_file = st.file_uploader("上传 TXT 文件", type=["txt"])
        if uploaded_file is not None:
            try:
                input_text = uploaded_file.read().decode("utf-8")
                st.session_state.input_text = input_text
                st.caption(f"已载入文件：{uploaded_file.name}")
            except UnicodeDecodeError:
                input_text = ""
                st.session_state.input_text = ""
                st.error("文件解码失败，当前仅支持 UTF-8 编码的 `.txt` 文件。")

    summary = build_summary(input_text)
    st.markdown("### 输入统计")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric("字符数", summary["total_chars"])
    with stat_col2:
        st.metric("字母数", summary["total_letters"])

    if summary["is_empty"]:
        st.caption("请先输入英文文本或上传 TXT 文件，然后点击“开始分析”。")
    elif summary["total_letters"] == 0:
        st.caption("已检测到输入内容，但其中不包含英文字母。")
    else:
        st.caption("当前输入可用于字母频率分析。")

    analyze = st.button(
        "开始分析",
        type="primary",
        use_container_width=True,
        disabled=bool(summary["is_empty"]),
    )

    if analyze:
        frequency_df, total_letters = build_frequency_table(input_text)
        st.session_state.analysis = {
            "data": frequency_df,
            "total_letters": total_letters,
            "source_text": input_text,
        }

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("结果")
    st.markdown(
        '<div class="section-note">先看结果摘要，再查看图表和详细数据。</div>',
        unsafe_allow_html=True,
    )

    analysis = st.session_state.analysis
    if analysis is None:
        render_empty_state("先在左侧输入或上传内容，再点击“开始分析”，结果会显示在这里。")
    else:
        data = analysis["data"].copy()
        total_letters = analysis["total_letters"]

        if total_letters == 0:
            render_empty_state("当前输入中没有可供统计的英文字母，请改用英文文本重新分析。")
        else:
            top_letter = data.iloc[0]
            bottom_letter = data.iloc[-1]
            insights = build_result_insights(data, total_letters)

            st.markdown(
                f"""
                <div class="summary-strip">
                    <div class="summary-card">
                        <div class="summary-label">总字母数</div>
                        <div class="summary-value">{total_letters}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">最高频字母</div>
                        <div class="summary-value">{top_letter["Letter"]} ({top_letter["Frequency"]:.2%})</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">最低频字母</div>
                        <div class="summary-value">{bottom_letter["Letter"]} ({bottom_letter["Frequency"]:.2%})</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            top_three_text = "，".join(
                f'{item["Letter"]}（{item["Frequency"]:.2%}）'
                for item in insights["top_three"]
            )
            st.markdown(f"**Top 3 字母：** {top_three_text}")

            if insights["short_sample"]:
                st.caption("样本较短，当前分布仅供参考。建议输入更长的英文文本以获得更稳定的结果。")
            elif insights["sparse_distribution"]:
                st.caption("当前输入中出现的有效字母种类较少，摘要仅反映这段文本的局部分布。")

            slider_col, label_col = st.columns([1.6, 1])
            with slider_col:
                top_n = st.slider("高亮前 N 个字母", min_value=1, max_value=10, value=5)
            with label_col:
                highlighted = "，".join(data.head(top_n)["Letter"].tolist())
                st.caption(f"当前高亮：{highlighted}")

            data["Group"] = "Top N"
            data.loc[top_n:, "Group"] = "Others"
            data.loc[: top_n - 1, "Group"] = "Top N"

            fig = px.bar(
                data,
                x="Letter",
                y="Frequency",
                color="Group",
                text=data["Frequency"].map(lambda value: f"{value:.2%}"),
                color_discrete_map={
                    "Top N": "#1f5c4a",
                    "Others": "#cfd7d2",
                },
                labels={
                    "Letter": "字母",
                    "Frequency": "频率",
                },
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(
                height=460,
                margin=dict(l=12, r=12, t=18, b=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(
                showgrid=True,
                gridcolor="rgba(31, 92, 74, 0.10)",
                tickformat=".0%",
                rangemode="tozero",
            )

            st.plotly_chart(fig, use_container_width=True)

            st.download_button(
                "下载 CSV",
                data=build_export_csv(data),
                file_name="letter_frequency_analysis.csv",
                mime="text/csv",
                use_container_width=True,
            )

            with st.expander("查看详细数据"):
                formatted = data[["Letter", "Count", "Frequency"]].copy()
                formatted["Frequency"] = formatted["Frequency"].map(lambda value: f"{value:.2%}")
                st.dataframe(formatted, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

