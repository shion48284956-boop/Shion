
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path
import html

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# =====================================
# 2. CSV 파일 불러오기
# =====================================

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "countriesMBTI_16types.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(CSV_PATH)
    return data

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

if "Country" not in df.columns:
    st.error("CSV에 Country 열이 없습니다.")
    st.stop()

mbti_columns = [c for c in df.columns if c != "Country"]

if len(mbti_columns) != 16:
    st.error("MBTI 유형이 16개인지 확인해주세요.")
    st.stop()

# =====================================
# 3. 화면 디자인
# =====================================

st.markdown("""
<style>
.stApp {
    background-color: #f7f9fc;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #1e3a8a;
}

.sub-title {
    color: #64748b;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 4. 제목
# =====================================

st.markdown(
    '<div class="main-title">🌍 국가별 MBTI 분석</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">국가를 선택하고 16가지 MBTI 비율을 분석해 보세요.</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# =====================================
# 5. 국가 선택
# =====================================

countries = sorted(df["Country"].dropna().unique())

selected_country = st.selectbox(
    "🏳️ 국가 선택",
    countries
)

# 선택 국가 데이터
country = df[df["Country"] == selected_country].iloc[0]

# =====================================
# 6. MBTI 비율 계산
# =====================================

result = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": [
        pd.to_numeric(country[c], errors="coerce")
        for c in mbti_columns
    ]
})

result["비율"] = result["비율"].fillna(0) * 100

result = result.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

# =====================================
# 7. 주요 정보
# =====================================

top_mbti = result.iloc[0]["MBTI"]
top_value = result.iloc[0]["비율"]

c1, c2, c3 = st.columns(3)

c1.metric("🌎 선택 국가", selected_country)
c2.metric("🏆 1위 MBTI", top_mbti)
c3.metric("📊 1위 비율", f"{top_value:.2f}%")

st.write("")
st.divider()

# =====================================
# 8. 그래프 제목
# =====================================

st.subheader(f"📊 {selected_country} MBTI 분포")

st.caption("비율이 높은 유형부터 1위~16위 순서로 표시됩니다.")

# =====================================
# 9. 색상 그라데이션
# =====================================

colors = [
    "#2563eb",
    "#3978e5",
    "#528ce9",
    "#6da1ed",
    "#86b4f0",
    "#9bc3f3",
    "#afd0f6",
    "#c1dcf8",
    "#d0e5fa",
    "#dcecfb",
    "#e3effc",
    "#e8f2fc",
    "#edf5fd",
    "#f0f6fd",
    "#f3f8fe"
]

# =====================================
# 10. 실제 막대그래프 HTML 생성
# =====================================

chart_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 18px;
    font-family: Arial, sans-serif;
    background: #ffffff;
}

.chart {
    width: 100%;
}

.bar-row {
    margin-bottom: 19px;
}

.bar-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 7px;
    font-size: 14px;
    color: #334155;
    font-weight: 600;
}

.bar-track {
    width: 100%;
    height: 17px;
    background: #edf2f7;
    border-radius: 20px;
    overflow: hidden;
}

.bar {
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}
</style>
</head>
<body>
<div class="chart">
"""

for i, row in result.iterrows():

    mbti = html.escape(str(row["MBTI"]))
    value = float(row["비율"])

    if i == 0:
        color = "#e53935"
        rank = "🥇 1위"
    else:
        color = colors[i - 1]
        rank = f"{i + 1}위"

    width = (
        value / top_value * 100
        if top_value > 0 else 0
    )

    chart_html += f"""
    <div class="bar-row">
        <div class="bar-info">
            <span>{rank}　{mbti}</span>
            <span>{value:.2f}%</span>
        </div>

        <div class="bar-track">
            <div class="bar"
                style="width:{width:.2f}%; background:{color};">
            </div>
        </div>
    </div>
    """

chart_html += """
</div>
</body>
</html>
"""

# 실제 그래프 출력
components.html(
    chart_html,
    height=850,
    scrolling=False
)

# =====================================
# 11. 전체 순위표
# =====================================

st.divider()

st.subheader("🏆 MBTI 전체 순위표")

display = result.copy()

display.insert(
    0,
    "순위",
    [f"{i}위" for i in range(1, 17)]
)

display["비율"] = display["비율"].apply(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)

# =====================================
# 12. 안내
# =====================================

st.info(
    "이 분석은 제공된 CSV 데이터의 수치를 바탕으로 합니다. "
    "국가 전체 국민의 실제 MBTI 분포를 확정하는 자료는 아닙니다."
)
