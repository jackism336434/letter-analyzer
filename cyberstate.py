from collections import Counter
import string

import pandas as pd
import plotly.express as px
import streamlit as st


def build_frequency_table(text: str) -> tuple[pd.DataFrame, int]:
    normalized = text.lower()
    letters = [char for char in normalized if char in string.ascii_lowercase]
    counter = Counter(letters)
    total_letters = len(letters)

    rows = []
    for letter in string.ascii_lowercase:
        count = counter.get(letter, 0)
        frequency = count / total_letters if total_letters else 0
        rows.append(
            {
                "Letter": letter.upper(),
                "Count": count,
                "Frequency": frequency,
            }
        )

    data = pd.DataFrame(rows).sort_values(
        by=["Frequency", "Count", "Letter"],
        ascending=[False, False, True],
        ignore_index=True,
    )
    return data, total_letters


def build_summary(text: str) -> dict[str, int]:
    total_chars = len(text)
    total_letters = sum(1 for char in text.lower() if char in string.ascii_lowercase)
    return {
        "total_chars": total_chars,
        "total_letters": total_letters,
        "is_empty": int(not text.strip()),
    }


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
            <strong>Result</strong><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="Letter Frequency Analyzer", layout="wide")
render_styles()

if "analysis" not in st.session_state:
    st.session_state.analysis = None

st.title("Letter Frequency Analyzer")
st.caption("统计英文文本字母频率，提供可视化结果分析。")

left_col, right_col = st.columns([1, 1.45], gap="large")

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Input")
    st.markdown(
        '<div class="section-note">选择输入方式，先看输入质量，再执行分析。</div>',
        unsafe_allow_html=True,
    )

    input_mode = st.radio(
        "输入方式",
        ("直接输入", "上传 TXT"),
        horizontal=True,
        label_visibility="collapsed",
    )

    input_text = ""
    if input_mode == "直接输入":
        input_text = st.text_area(
            "输入英文文本",
            placeholder="Paste or type English text here...",
            height=260,
            label_visibility="collapsed",
        )
    else:
        uploaded_file = st.file_uploader("上传 TXT 文件", type=["txt"])
        if uploaded_file is not None:
            try:
                input_text = uploaded_file.read().decode("utf-8")
                st.caption(f"已载入文件: {uploaded_file.name}")
            except UnicodeDecodeError:
                input_text = ""
                st.error("文件解码失败，目前仅支持 UTF-8 编码的 .txt 文件。")

    summary = build_summary(input_text)
    st.markdown("### 输入统计")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric("字符数 Chars", summary["total_chars"])
    with stat_col2:
        st.metric("字母数 Letters", summary["total_letters"])

    if summary["is_empty"]:
        st.caption("当前没有可分析内容。")
    elif summary["total_letters"] == 0:
        st.caption("已检测到输入，但没有英文字符。")
    else:
        st.caption("输入可用于频率分析。")

    analyze = st.button(
        "Analyze",
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
    st.subheader("Results")
    st.markdown(
        '<div class="section-note">摘要优先，图表其次，详细数据默认折叠。</div>',
        unsafe_allow_html=True,
    )

    analysis = st.session_state.analysis
    if analysis is None:
        render_empty_state("在左侧输入文本或上传文件后，点击 Analyze 查看结果。")
    else:
        data = analysis["data"].copy()
        total_letters = analysis["total_letters"]

        if total_letters == 0:
            render_empty_state("当前输入没有可统计的英文字符，请改用英文文本再分析。")
        else:
            top_letter = data.iloc[0]
            bottom_letter = data.iloc[-1]

            st.markdown(
                f"""
                <div class="summary-strip">
                    <div class="summary-card">
                        <div class="summary-label">Total Letters</div>
                        <div class="summary-value">{total_letters}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">Top Letter</div>
                        <div class="summary-value">{top_letter["Letter"]} ({top_letter["Frequency"]:.2%})</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">Lowest Letter</div>
                        <div class="summary-value">{bottom_letter["Letter"]} ({bottom_letter["Frequency"]:.2%})</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            slider_col, label_col = st.columns([1.6, 1])
            with slider_col:
                top_n = st.slider("Top N 高亮", min_value=1, max_value=10, value=5)
            with label_col:
                highlighted = ", ".join(data.head(top_n)["Letter"].tolist())
                st.caption(f"Highlight: {highlighted}")

            data["Group"] = "Top N"  # default value overwritten below
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
                    "Letter": "Letter",
                    "Frequency": "Frequency",
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

            with st.expander("查看详细数据 / Detailed Data"):
                formatted = data[["Letter", "Count", "Frequency"]].copy()
                formatted["Frequency"] = formatted["Frequency"].map(lambda value: f"{value:.2%}")
                st.dataframe(formatted, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)
