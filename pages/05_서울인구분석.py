
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import re
import math

# 페이지 설정
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령별 인구 분석")
st.write("행정구역, 연도, 성별을 선택하여 연령대별 인구를 분석해 보세요.")

# CSV 경로 설정
# 현재 파일은 pages 폴더 안에 있으므로 상위 폴더로 이동
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "population.csv")


# 데이터 불러오기
@st.cache_data
def load_data():
    # 한글 깨짐 방지
    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # 숫자 데이터 변환
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )

    # 행정구역 이름 추출
    df["행정구역명"] = (
        df["행정구역"]
        .astype(str)
        .str.extract(r"서울특별시\s*(.*?)\s*\(\d+\)")[0]
        .fillna("")
        .str.strip()
    )

    # 서울시 전체 이름 처리
    df.loc[
        df["행정구역명"] == "",
        "행정구역명"
    ] = "서울특별시 전체"

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# 행정구역 선택
st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

district_list = df["행정구역명"].drop_duplicates().tolist()

with col1:
    district = st.selectbox(
        "행정구역 선택",
        district_list
    )

with col2:
    year = st.selectbox(
        "연도 선택",
        ["2020", "2021", "2022", "2023", "2024", "2025"]
    )

with col3:
    gender = st.selectbox(
        "성별 선택",
        ["전체", "남성", "여성"]
    )


# 성별 및 연도에 따른 컬럼 이름 설정
gender_prefix = {
    "전체": "",
    "남성": "남_",
    "여성": "여_"
}

prefix = f"{year}년_{gender_prefix[gender]}거주자_"


# 연령대 컬럼 찾기
age_columns = []

for col in df.columns:
    if col.startswith(prefix):
        age = col[len(prefix):]

        if re.fullmatch(r"\d+~\d+세|\d+세 이상", age):
            age_columns.append(col)


# 연령대 순서 정렬
def age_sort(col):
    age = col[len(prefix):]
    return int(re.search(r"\d+", age).group())


age_columns = sorted(age_columns, key=age_sort)


if not age_columns:
    st.error(
        f"{year}년 {gender} 연령대 데이터를 찾을 수 없습니다. "
        "CSV 컬럼 이름을 확인해 주세요."
    )
    st.stop()


# 선택한 행정구역 데이터
selected_data = df[
    df["행정구역명"] == district
]

if selected_data.empty:
    st.error("선택한 행정구역 데이터가 없습니다.")
    st.stop()


# 그래프 데이터 생성
ages = [
    col[len(prefix):]
    for col in age_columns
]

values = (
    selected_data.iloc[0][age_columns]
    .fillna(0)
    .astype(int)
    .tolist()
)

chart_df = pd.DataFrame({
    "나이": ages,
    "인구수": values
})


# 그래프 제목
st.divider()

st.subheader(
    f"📈 {district} {year}년 {gender} 연령별 인구"
)


# 세로축 최대값 설정
max_population = max(values)

y_max = max(
    1000,
    math.ceil(max_population / 1000) * 1000
)


# 꺾은선 그래프
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["나이"],
        y=chart_df["인구수"],
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="#16A34A",
            width=3
        ),
        marker=dict(
            color="#16A34A",
            size=8
        ),
        hovertemplate=(
            "나이: %{x}<br>"
            "인구수: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)


# 그래프 디자인
fig.update_layout(
    height=550,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        family="Malgun Gothic, Arial, sans-serif",
        size=13,
        color="#333333"
    ),
    xaxis=dict(
        title="나이",
        showgrid=False
    ),
    yaxis=dict(
        title="인구수 (명)",
        range=[0, y_max],
        tickmode="linear",
        tick0=0,
        dtick=1000,
        tickformat=",",
        showgrid=True,
        gridcolor="#DDDDDD",
        gridwidth=1,
        zeroline=True
    ),
    margin=dict(
        l=80,
        r=30,
        t=40,
        b=60
    ),
    showlegend=False
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# 데이터 표
st.subheader("📋 연령대별 인구 데이터")

display_df = chart_df.copy()

display_df["인구수"] = display_df["인구수"].map(
    lambda x: f"{x:,}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# 분석 결과
st.subheader("📌 분석 결과")

max_index = values.index(max_population)

st.success(
    f"가장 인구가 많은 연령대는 "
    f"{ages[max_index]}이며, "
    f"인구수는 {max_population:,}명입니다."
)

st.caption(
    "자료 출처: 서울특별시 인구 데이터"
)
