
from pathlib import Path
import html

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="국가별 MBTI 분석", layout="wide")

# CSV 파일 경로
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "countriesMBTI_16types.csv"

st.title("🌍 국가별 MBTI 분포 분석")
st.write("국가를 선택하면 16가지 MBTI 유형의 비율을 막대 그래프로 보여줍니다.")

# 데이터 불러오기
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    st.error(f"CSV 파일을 불러오지 못했습니다: {e}")
    st.stop()

if "Country" not in df.columns:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()

mbti_columns = [c for c in df.columns if c != "Country"]

country = st.selectbox(
    "국가 선택",
    sorted(df["Country"].dropna().unique())
)

selected = df[df["Country"] == country].iloc[0]

# MBTI 비율 정리
data = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": [pd.to_numeric(selected[c], errors="coerce") for c in mbti_columns]
}).dropna()

data["비율"] = data["비율"] * 100
data = data.sort_values("비율", ascending=False).reset_index(drop=True)

st.subheader(f"📊 {country}의 MBTI 유형별 비율")

# 순위별 색상
colors = ["#e53935"] + [
    f"#{int(30 + i * 10):02x}{int(110 + i * 8):02x}{int(220 + i * 2):02x}"
    for i in range(15)
]

# 막대 그래프 HTML
bars = ""

max_value = max(data["비율"].max(), 1)

for i, row in data.iterrows():
    mbti = html.escape(str(row["MBTI"]))
    value = row["비율"]
    width = value / max_value * 100
    color = colors[i]

    bars += f"""
    <div class="bar-row">
        <div class="rank">{i + 1}위</div>
        <div class="mbti">{mbti}</div>
        <div class="bar-area">
            <div class="bar" style="width:{width}%; background:{color};"></div>
        </div>
        <div class="percent">{value:.2f}%</div>
    </div>
    """

chart_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 10px;
    color: #333;
}}
.bar-row {{
    display: flex;
    align-items: center;
    margin: 13px 0;
    gap: 10px;
}}
.rank {{
    width: 38px;
    font-weight: bold;
    font-size: 14px;
}}
.mbti {{
    width: 55px;
    font-weight: bold;
    font-size: 14px;
}}
.bar-area {{
    flex: 1;
    height: 23px;
    background: #eeeeee;
    border-radius: 5px;
    overflow: hidden;
}}
.bar {{
    height: 100%;
    border-radius: 5px;
}}
.percent {{
    width: 65px;
    text-align: right;
    font-size: 13px;
    font-weight: bold;
}}
</style>
</head>
<body>
{bars}
</body>
</html>
"""

components.html(chart_html, height=700, scrolling=True)

st.subheader("🏆 MBTI 순위표")
ranking = data.copy()
ranking.index = ranking.index + 1
ranking.index.name = "순위"
ranking = ranking.rename(columns={"비율": "비율(%)"})
st.dataframe(ranking, use_container_width=True)
