
import streamlit as st
import pandas as pd
import html
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# =====================================
# 1. CSV 파일 경로 설정
# =====================================

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "countriesMBTI_16types.csv"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.write("상위 폴더에 countriesMBTI_16types.csv 파일이 있는지 확인해주세요.")
    st.stop()

# =====================================
# 2. 기본 데이터 확인
# =====================================

if "Country" not in df.columns:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()

mbti_columns = [
    col for col in df.columns if col != "Country"
]

if len(mbti_columns) != 16:
    st.error("MBTI 데이터가 16개인지 확인해주세요.")
    st.stop()

# =====================================
# 3. 디자인 설정
# =====================================

st.markdown("""
<style>
.main {
    background-color: #f8faff;
}

.title {
    font-size: 34px;
    font-weight: 800;
    color: #1e3a8a;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.chart-container {
    background: white;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
}

.bar-row {
    margin-bottom: 17px;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 14px;
    font-weight: 600;
    color: #334155;
}

.bar-bg {
    width: 100%;
    height: 15px;
    background: #edf2f7;
    border-radius: 20px;
    overflow: hidden;
}

.bar-fill {
    height: 15px;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 4. 제목
# =====================================

st.markdown(
    '<div class="title">🌍 국가별 MBTI 분석</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">158개 국가의 MBTI 분포를 한눈에 확인해 보세요.</div>',
    unsafe_allow_html=True
)

st.write("")

# =====================================
# 5. 국가 선택
# =====================================

country_list = sorted(
    df["Country"].dropna().unique()
)

selected_country = st.selectbox(
    "🏳️ 분석하고 싶은 국가를 선택하세요.",
    country_list
)

# 선택한 국가 데이터
country_data = df[
    df["Country"] == selected_country
].iloc[0]

# =====================================
# 6. MBTI 비율 계산
# =====================================

result = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": [
        float(country_data[mbti]) * 100
        for mbti in mbti_columns
    ]
})

# 비율 높은 순서대로 정렬
result = result.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)

# =====================================
# 7. 주요 정보
# =====================================

top_mbti = result.iloc[0]["MBTI"]
top_value = result.iloc[0]["비율"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "선택 국가",
        selected_country
    )

with col2:
    st.metric(
        "가장 높은 MBTI",
        top_mbti
    )

with col3:
    st.metric(
        "1위 비율",
        f"{top_value:.2f}%"
    )

st.write("")

# =====================================
# 8. 막대그래프
# =====================================

st.subheader(f"📊 {selected_country}의 MBTI 비율")

st.caption(
    "MBTI 16가지 유형을 비율이 높은 순서대로 정렬했습니다."
)

# 파란색 그라데이션
blue_colors = [
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

chart_html = '<div class="chart-container">'

for index, row in result.iterrows():

    mbti = html.escape(str(row["MBTI"]))
    value = row["비율"]

    # 1위는 빨간색
    if index == 0:
        color = "#e53935"
        rank = "🥇 1위"

    # 2위부터 파란색 그라데이션
    else:
        color = blue_colors[index - 1]
        rank = f"{index + 1}위"

    # 막대 길이 계산
    bar_width = (
        value / top_value * 100
        if top_value > 0 else 0
    )

    chart_html += f"""
    <div class="bar-row">

        <div class="bar-label">
            <span>{rank}　{mbti}</span>
            <span>{value:.2f}%</span>
        </div>

        <div class="bar-bg">
            <div class="bar-fill"
                style="
                    width: {bar_width:.2f}%;
                    background: {color};
                ">
            </div>
        </div>

    </div>
    """

chart_html += "</div>"

st.markdown(
    chart_html,
    unsafe_allow_html=True
)

# =====================================
# 9. 전체 순위표
# =====================================

st.write("")
st.subheader("🏆 MBTI 전체 순위")

display_data = result.copy()

display_data.insert(
    0,
    "순위",
    [f"{i}위" for i in range(1, 17)]
)

display_data["비율"] = display_data["비율"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)

# =====================================
# 10. 안내 문구
# =====================================

st.info(
    "※ 제공된 CSV 데이터를 기준으로 국가별 MBTI 비율을 비교합니다. "
    "실제 국민 전체의 성격 분포를 확정하는 통계는 아닙니다."
)
