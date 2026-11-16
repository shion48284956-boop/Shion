
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("월을 선택하여 연도별 최고기온과 최저기온을 비교해 보세요.")

# CSV 파일 불러오기 (CP949 한글 인코딩)
@st.cache_data
def load_data():
    df = pd.read_csv("temperature (2).csv", encoding="cp949")

    # 날짜 데이터 변환
    df["날짜"] = pd.to_datetime(
        df["일시"],
        format="%b-%y",
        errors="coerce"
    )

    # 연도와 월 추출
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    return df.dropna(subset=["날짜"])

df = load_data()

# 월 선택
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

selected_month = st.selectbox(
    "📅 분석할 월을 선택하세요",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x]
)

# 선택한 월의 데이터 추출
filtered_df = df[df["월"] == selected_month].copy()
filtered_df = filtered_df.sort_values("연도")

if not filtered_df.empty:

    # 꺾은선 그래프 생성
    fig = go.Figure()

    # 최고기온
    fig.add_trace(go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="hotpink", width=3),
        marker=dict(size=8)
    ))

    # 최저기온
    fig.add_trace(go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="skyblue", width=3),
        marker=dict(size=8)
    ))

    # 그래프 제목 및 축 설정
    fig.update_layout(
        title="월별 기온분석",
        xaxis_title="연도",
        yaxis_title="온도 (℃)",
        legend_title="기온 구분",
        template="plotly_white",
        hovermode="x unified",
        height=550
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표 출력
    st.subheader("📊 기온 데이터")

    result = filtered_df[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].copy()

    result.columns = ["연도", "최고기온(℃)", "최저기온(℃)"]

    st.dataframe(result, use_container_width=True)

else:
    st.warning("선택한 월의 데이터가 없습니다.")
