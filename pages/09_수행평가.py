
import streamlit as st
import pandas as pd
import os

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="FIT PICK",
    page_icon="💪",
    layout="wide"
)

# =====================================
# 2. CSV 파일 불러오기
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "FIT_PICK_운동추천.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(
        CSV_PATH,
        encoding="utf-8-sig"
    )

try:
    df = load_data()

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.error("FIT_PICK_운동추천.csv 파일이 최상위 폴더에 있는지 확인하세요.")
    st.stop()

# =====================================
# 3. 제목 및 소개
# =====================================

st.title("💪 FIT PICK")
st.subheader("나에게 맞는 근육 부위별 운동 추천")

st.write(
    "운동하고 싶은 근육 부위를 입력하면 "
    "대표 운동 3가지를 추천해 드립니다."
)

st.divider()

# =====================================
# 4. 근육 부위 및 검색어 설정
# =====================================

aliases = {
    "가슴": ["가슴", "가슴근육", "흉근"],
    "등": ["등", "등근육", "광배근"],
    "어깨": ["어깨", "어깨근육", "삼각근"],
    "이두근": ["이두근", "이두", "팔 앞쪽"],
    "삼두근": ["삼두근", "삼두", "팔 뒤쪽"],
    "복부": ["복부", "복근", "배", "배근육"],
    "엉덩이": ["엉덩이", "엉덩이근육", "둔근"],
    "허벅지 앞쪽": [
        "허벅지 앞쪽",
        "허벅지 앞",
        "앞벅지"
    ],
    "허벅지 뒤쪽": [
        "허벅지 뒤쪽",
        "허벅지 뒤",
        "햄스트링"
    ],
    "종아리": ["종아리", "종아리근육"]
}

# =====================================
# 5. 운동 부위 입력
# =====================================

st.header("🔍 1. 운동할 부위를 입력하세요")

with st.form("search_form"):

    user_input = st.text_input(
        "근육 부위 입력",
        placeholder="예: 가슴, 등, 어깨, 복부"
    )

    search_button = st.form_submit_button(
        "운동 추천받기 💪",
        use_container_width=True
    )

if search_button:

    search_text = (
        user_input.strip()
        .replace(" ", "")
        .lower()
    )

    selected_part = None

    for part, words in aliases.items():

        normalized_words = [
            word.replace(" ", "").lower()
            for word in words
        ]

        if search_text in normalized_words:
            selected_part = part
            break

    if selected_part:

        st.session_state["selected_part"] = selected_part

    else:

        st.session_state["selected_part"] = None

        if search_text:
            st.warning(
                "해당 부위를 찾을 수 없습니다. "
                "등록된 근육 부위를 입력해 주세요."
            )
        else:
            st.warning("운동할 부위를 입력해 주세요.")

# =====================================
# 6. 추천 가능한 운동 부위
# =====================================

if not st.session_state.get("selected_part"):

    st.subheader("📌 추천 가능한 운동 부위")

    parts = list(aliases.keys())

    cols = st.columns(5)

    for i, part in enumerate(parts):

        with cols[i % 5]:

            if st.button(
                part,
                key=f"part_{i}",
                use_container_width=True
            ):

                st.session_state["selected_part"] = part
                st.rerun()

# =====================================
# 7. 추천 운동 3개 출력
# =====================================

if st.session_state.get("selected_part"):

    part = st.session_state["selected_part"]

    result = df[
        df["운동부위"].astype(str).str.strip() == part
    ]

    st.divider()

    st.header(f"🏋️ 2. {part} 추천 운동 TOP 3")

    if len(result) == 0:

        st.warning("해당 부위의 운동 데이터가 없습니다.")

    else:

        if len(result) != 3:
            st.warning(
                f"현재 해당 부위의 운동 데이터는 {len(result)}개입니다."
            )

        cols = st.columns(3)

        for i, (_, row) in enumerate(result.iterrows()):

            with cols[i]:

                st.markdown(f"### 추천 {i+1}")

                st.subheader(row["운동명"])

                st.write(
                    f"**주요 사용 근육**\n\n"
                    f"{row['주요_사용_근육']}"
                )

                st.caption(
                    f"필요 기구: {row['필요_기구']}"
                )

    # =================================
    # 8. 운동 선택
    # =================================

    if len(result) > 0:

        st.divider()

        st.header("🎯 3. 자세히 알아볼 운동 선택")

        exercise_names = result["운동명"].tolist()

        selected_exercise = st.selectbox(
            "원하는 운동을 선택하세요.",
            exercise_names
        )

        detail = result[
            result["운동명"] == selected_exercise
        ].iloc[0]

        # =================================
        # 9. 운동 상세 정보
        # =================================

        st.divider()

        st.header("📖 4. 운동 상세 정보")

        st.title(f"💪 {detail['운동명']}")

        st.info(
            f"주요 사용 근육: {detail['주요_사용_근육']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🛠️ 필요한 운동 기구")

            st.write(detail["필요_기구"])

        with col2:

            st.subheader("📍 시작 자세")

            st.write(detail["시작_자세"])

        st.divider()

        st.subheader("📚 자세한 운동 방법")

        st.write(detail["자세한_운동_방법"])

        st.divider()

        st.subheader("🌬️ 올바른 호흡법")

        st.write(detail["호흡법"])

        st.divider()

        st.subheader("⚠️ 운동 시 주의사항")

        st.warning(detail["주의사항"])

        st.divider()

        st.subheader("🌱 초보자를 위한 운동 팁")

        st.success(detail["초보자_팁"])

        st.divider()

        # =================================
        # 10. 다른 운동 부위 검색
        # =================================

        if st.button(
            "🔄 다른 근육 부위 검색하기",
            use_container_width=True
        ):

            st.session_state["selected_part"] = None
            st.rerun()

# =====================================
# 11. 하단 안내
# =====================================

st.divider()

st.caption(
    "FIT PICK | 근육 부위별 맞춤 운동 추천 서비스"
)

st.caption(
    "정확한 자세와 안전을 우선으로 운동하세요."
)
st.subheader("📊 부위별 운동 개수")

chart_data = df["운동부위"].value_counts()

st.bar_chart(chart_data)
