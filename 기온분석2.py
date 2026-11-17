
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pathlib import Path

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 분석 및 예측")
st.write("과거 기온 데이터를 이용하여 선형회귀 알고리즘으로 미래 기온을 예측합니다.")

# 한글 폰트 설정
plt.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------
# CSV 파일 불러오기
# -----------------------------
@st.cache_data
def load_data():
    file_candidates = [
        Path("temperature.csv"),
        Path("temperature (1).csv")
    ]

    file_path = next(
        (p for p in file_candidates if p.exists()),
        None
    )

    if file_path is None:
        raise FileNotFoundError(
            "temperature.csv 파일을 app.py와 같은 폴더에 넣어주세요."
        )

    encodings = ["cp949", "utf-8-sig", "utf-8"]

    for encoding in encodings:
        try:
            data = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV 파일의 인코딩을 확인해주세요.")

    required_columns = ["일시", "평균기온(℃)"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"CSV 파일에 {column} 열이 없습니다.")

    # 날짜 데이터 변환
    data["날짜"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    )

    data["연도"] = data["연도"].astype(int)
    data["월"] = data["월"].astype(int)

    return data.sort_values("날짜")


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

# -----------------------------
# 월 선택 및 예측 연도 선택
# -----------------------------
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

st.subheader("📌 분석 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월 선택",
        list(month_names.keys()),
        format_func=lambda x: month_names[x]
    )

with col2:
    latest_year = int(df["연도"].max())

    selected_year = st.number_input(
        "예측 연도 선택",
        min_value=latest_year + 1,
        max_value=2100,
        value=latest_year + 1,
        step=1
    )

# -----------------------------
# 선택한 월의 데이터 추출
# -----------------------------
month_data = df[df["월"] == selected_month].copy()

month_data = month_data.dropna(
    subset=["연도", "평균기온(℃)"]
)

if len(month_data) < 2:
    st.error("예측에 필요한 데이터가 부족합니다.")
    st.stop()

X = month_data[["연도"]]
y = month_data["평균기온(℃)"]

# -----------------------------
# 선형회귀 모델 학습
# -----------------------------
model = LinearRegression()
model.fit(X, y)

# 선택한 연도 예측
prediction = model.predict(
    pd.DataFrame({"연도": [selected_year]})
)[0]

# 회귀식 계수
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

# -----------------------------
# 예측 결과
# -----------------------------
st.divider()
st.subheader("📊 평균기온 예측 결과")

result1, result2, result3 = st.columns(3)

with result1:
    st.metric(
        "선택한 월",
        month_names[selected_month]
    )

with result2:
    st.metric(
        "예측 연도",
        f"{selected_year}년"
    )

with result3:
    st.metric(
        "예측 평균기온",
        f"{prediction:.2f} ℃"
    )

st.caption(
    f"과거 {len(month_data)}개의 데이터를 학습하여 예측한 결과입니다."
)

# -----------------------------
# 1. 과거 평균기온 + 예측기온 그래프
# -----------------------------
st.subheader("1️⃣ 연도별 평균기온 및 미래 예측")

fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(
    month_data["연도"],
    month_data["평균기온(℃)"],
    marker="o",
    linewidth=2,
    label="실제 평균기온"
)

ax1.scatter(
    selected_year,
    prediction,
    color="red",
    s=130,
    marker="*",
    label="예측 평균기온",
    zorder=5
)

ax1.plot(
    [latest_year, selected_year],
    [
        model.predict(pd.DataFrame({"연도": [latest_year]}))[0],
        prediction
    ],
    linestyle="--",
    color="red",
    alpha=0.7,
    label="예측 구간"
)

ax1.annotate(
    f"{prediction:.2f}℃",
    (selected_year, prediction),
    xytext=(8, 12),
    textcoords="offset points",
    color="red",
    fontsize=11
)

ax1.set_title(
    f"{month_names[selected_month]} 연도별 평균기온 분석 및 예측",
    fontsize=15
)
ax1.set_xlabel("연도")
ax1.set_ylabel("평균기온 (℃)")
ax1.grid(True, alpha=0.3)
ax1.legend()
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

# -----------------------------
# 2. 선형회귀 알고리즘 시각화
# -----------------------------
st.divider()
st.subheader("2️⃣ 선형회귀 알고리즘 작동 과정")

st.write(
    "선형회귀는 과거의 연도별 평균기온 데이터를 바탕으로 "
    "가장 적합한 직선을 찾아 미래의 기온을 예측하는 방법입니다."
)

# 회귀선에 사용할 연도 생성
line_years = np.linspace(
    month_data["연도"].min(),
    selected_year,
    300
)

line_predictions = model.predict(
    pd.DataFrame({"연도": line_years})
)

fig2, ax2 = plt.subplots(figsize=(12, 5))

# 실제 데이터
ax2.scatter(
    X["연도"],
    y,
    color="blue",
    s=55,
    label="실제 관측 데이터"
)

# 회귀 직선
ax2.plot(
    line_years,
    line_predictions,
    color="red",
    linewidth=2.5,
    label="선형회귀 예측 직선"
)

# 미래 예측 지점
ax2.scatter(
    selected_year,
    prediction,
    color="green",
    marker="*",
    s=180,
    label="미래 예측 지점",
    zorder=5
)

# 실제값과 회귀선 사이의 오차 표현
for year, actual, predicted in zip(
    X["연도"],
    y,
    model.predict(X)
):
    ax2.vlines(
        year,
        min(actual, predicted),
        max(actual, predicted),
        color="gray",
        alpha=0.25,
        linewidth=1
    )

ax2.set_title(
    "선형회귀 알고리즘의 학습 및 예측 과정",
    fontsize=15
)
ax2.set_xlabel("연도")
ax2.set_ylabel("평균기온 (℃)")
ax2.grid(True, alpha=0.3)
ax2.legend()
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

# -----------------------------
# 회귀식과 학습 결과
# -----------------------------
st.subheader("📐 선형회귀 학습 결과")

st.latex(
    rf"\hat{{y}} = {slope:.4f}x + ({intercept:.4f})"
)

col1, col2 = st.columns(2)

with col1:
    st.metric("기울기", f"{slope:.4f}")

with col2:
    st.metric("결정계수 (R²)", f"{r2:.4f}")

st.caption(
    "결정계수(R²)는 모델이 과거 기온 데이터의 변화를 "
    "얼마나 설명하는지 나타내는 값입니다. "
    "1에 가까울수록 과거 데이터에 대한 설명력이 높습니다."
)

# -----------------------------
# 3. 선형회귀 알고리즘 쉬운 설명
# -----------------------------
st.divider()
st.subheader("📖 선형회귀 알고리즘이란?")

st.markdown("""
**선형회귀**는 두 가지 데이터 사이의 관계를 직선으로 나타내어
앞으로의 값을 예측하는 머신러닝 알고리즘입니다.

이번 프로그램에서는 과거의 연도와 평균기온 사이의 관계를 학습합니다.

**① 데이터 수집**

선택한 월에 해당하는 과거 모든 연도의 평균기온을 모읍니다.

**② 직선 찾기**

실제 기온 데이터와 가장 가까운 직선을 찾습니다.
이때 실제 기온과 직선이 예측한 기온 사이의 차이를
제곱하여 모두 더한 값이 최소가 되도록 직선을 결정합니다.

**③ 미래 기온 예측**

찾아낸 직선에 사용자가 선택한 미래 연도를 넣어
해당 월의 평균기온을 계산합니다.

**④ 결과 확인**

실제 기온 그래프와 예측 기온을 비교하여
과거 기온의 변화와 미래 예측 결과를 확인할 수 있습니다.
""")

st.info(
    "참고: 이 프로그램은 과거의 연도별 기온 추세를 직선으로 "
    "학습합니다. 계절별 반복 변화나 장기적인 기후 요인을 "
    "모두 반영하지 않으므로 미래 예측값은 실제 기온과 다를 수 있습니다."
)

# -----------------------------
# 데이터 확인
# -----------------------------
with st.expander("📋 선택한 월의 실제 데이터 확인"):
    display_data = month_data[
        ["연도", "평균기온(℃)"]
    ].copy()

    st.dataframe(
        display_data.sort_values("연도"),
        use_container_width=True,
        hide_index=True
    )
