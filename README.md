# CyberTool

一个基于 Streamlit 的小型应用，用于分析英文文本中的字母频率，并以可视化方式展示结果。

## 主入口

主应用入口为：

```bash
streamlit run cyberstate.py
```

## 功能说明

- 支持直接粘贴英文文本或上传 UTF-8 编码的 `.txt` 文件
- 统计 `A-Z` 的出现次数和频率
- 支持高亮前 N 个高频字母
- 展示摘要指标和 Top 3 字母
- 支持将结果导出为 CSV
- 在样本较短时给出提示

## 依赖要求

- Python 3.10+
- `streamlit`
- `plotly`
- `pandas`
- `numpy`
- `pytest`（用于运行测试）

安装依赖：

```bash
pip install -r requirements.txt
```

## 本地开发

启动应用：

```bash
streamlit run cyberstate.py
```

执行不落地字节码的语法检查：

```bash
@'
from pathlib import Path
for path in ["analyzer.py", "cyberstate.py", "tests/test_analyzer.py"]:
    source = Path(path).read_text(encoding="utf-8")
    compile(source, path, "exec")
print("syntax-ok")
'@ | python -
```

运行测试：

```bash
pytest
```

## 手动验证建议

发布前至少检查以下场景：

- 直接输入英文文本后可以正常分析
- 上传 UTF-8 编码的 `.txt` 文件后可以正常载入并分析
- 上传非 UTF-8 文件时会给出清晰报错
- 空输入、无英文字母输入、短文本输入时提示正确
- 下载 CSV 后字段仍然是 `Letter`、`Count`、`Frequency`

## 部署准备

当前仓库暂时保持平台中立，后续可根据需要接入：

- Streamlit Community Cloud
- Docker 自部署
- 内部 Python 应用托管环境

最小部署要求是目标环境能够安装 `requirements.txt` 中的依赖，并执行 `streamlit run cyberstate.py`。
