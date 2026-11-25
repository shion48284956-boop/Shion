
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

# 필요한 CSV 열 확인
required_columns = [
    "운동부위",
    "운동명",
    "주요_사용_근육",
    "필요_기구",
    "시작_자세",
    "자세한_운동_방법",
    "호흡법",
    "주의사항",
    "초보자_팁"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"CSV에 필요한 항목이 없습니다: {missing_columns}")
    st.stop()

# =====================================
# 3. 운동별 추천 정보
# =====================================

exercise_plan = {
    "체스트 프레스 머신": {
        "세트": 2, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "가슴 근육을 중심으로 상체 밀기 동작을 익히기 좋은 운동입니다."
    },
    "푸시업": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "초급",
        "이유": "가슴과 팔 그리고 몸통의 안정성을 함께 기를 수 있습니다."
    },
    "펙덱 플라이 머신": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "가슴 근육을 모으는 움직임에 집중할 수 있습니다."
    },

    "랫풀다운": {
        "세트": 3, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "등의 넓은 근육을 사용하며 당기는 동작을 익힐 수 있습니다."
    },
    "시티드 케이블 로우": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "등 중앙과 어깨 주변 근육을 함께 사용하는 운동입니다."
    },
    "원암 덤벨 로우": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "한쪽씩 운동하며 등 근육의 움직임을 집중해서 느낄 수 있습니다."
    },

    "숄더 프레스 머신": {
        "세트": 2, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "어깨 근육을 중심으로 팔을 위로 미는 동작을 연습할 수 있습니다."
    },
    "사이드 레터럴 레이즈": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "중급",
        "이유": "어깨 옆쪽 근육의 움직임에 집중할 수 있습니다."
    },
    "페이스 풀": {
        "세트": 2, "횟수": 10, "단위": "회",
        "난이도": "중급",
        "이유": "어깨 뒤쪽과 등 위쪽 근육을 함께 사용하는 운동입니다."
    },

    "덤벨 컬": {
        "세트": 2, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "이두근을 중심으로 팔을 굽히는 동작을 익힐 수 있습니다."
    },
    "해머 컬": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "이두근과 팔뚝 근육을 함께 사용하는 운동입니다."
    },
    "케이블 컬": {
        "세트": 3, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "케이블 저항을 이용해 팔을 굽히는 동작을 연습할 수 있습니다."
    },

    "케이블 푸시다운": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "삼두근을 중심으로 팔꿈치를 펴는 동작을 익힐 수 있습니다."
    },
    "오버헤드 케이블 익스텐션": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "팔을 머리 위로 올린 자세에서 삼두근을 사용할 수 있습니다."
    },
    "무릎 대고 좁은 푸시업": {
        "세트": 2, "횟수": 6, "단위": "회",
        "난이도": "중급",
        "이유": "팔 간격을 좁혀 삼두근 사용에 집중하는 운동입니다."
    },

    "플랭크": {
        "세트": 2, "횟수": 20, "단위": "초",
        "난이도": "초급",
        "이유": "복부와 몸통의 안정성을 유지하는 연습에 적합합니다."
    },
    "데드버그": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "초급",
        "이유": "팔과 다리를 교차로 움직이며 몸통을 안정적으로 유지하는 운동입니다."
    },
    "버드독": {
        "세트": 3, "횟수": 8, "단위": "회",
        "난이도": "초급",
        "이유": "몸통의 균형과 안정성을 연습하기 좋은 운동입니다."
    },

    "글루트 브리지": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "엉덩이 근육을 중심으로 골반을 들어 올리는 동작입니다."
    },
    "힙 어브덕션 머신": {
        "세트": 3, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "엉덩이 옆쪽 근육을 사용하는 운동입니다."
    },
    "스텝업": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "한쪽 다리씩 체중을 지지하며 엉덩이와 허벅지를 사용합니다."
    },

    "레그 익스텐션": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "허벅지 앞쪽 근육을 중심으로 무릎을 펴는 운동입니다."
    },
    "고블릿 스쿼트": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "허벅지와 엉덩이를 함께 사용하며 스쿼트 자세를 익힐 수 있습니다."
    },
    "레그 프레스": {
        "세트": 3, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "기구를 이용해 허벅지와 엉덩이 근육을 사용하는 운동입니다."
    },

    "레그 컬 머신": {
        "세트": 2, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "허벅지 뒤쪽 근육을 중심으로 무릎을 굽히는 운동입니다."
    },
    "맨몸 힙 힌지": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "엉덩이를 뒤로 보내는 움직임과 올바른 자세를 연습할 수 있습니다."
    },

    "스탠딩 카프 레이즈": {
        "세트": 2, "횟수": 12, "단위": "회",
        "난이도": "초급",
        "이유": "서 있는 자세에서 종아리 근육을 사용하는 운동입니다."
    },
    "시티드 카프 레이즈": {
        "세트": 3, "횟수": 10, "단위": "회",
        "난이도": "초급",
        "이유": "앉은 자세에서 종아리 근육의 움직임에 집중할 수 있습니다."
    },
    "계단 카프 레이즈": {
        "세트": 2, "횟수": 8, "단위": "회",
        "난이도": "중급",
        "이유": "발뒤꿈치의 움직임 범위를 조절하며 종아리를 사용하는 운동입니다."
    }
}

# =====================================
# 4. 제목 및 소개
# =====================================

st.title("💪 FIT PICK")
st.subheader("나에게 맞는 근육 부위별 운동 추천")

st.write(
    "운동하고 싶은 근육 부위를 선택하면 "
    "대표 운동과 자세한 운동 정보를 추천해 드립니다."
)

st.info(
    "💡 원하는 운동 부위를 검색하고 "
    "나에게 맞는 운동 방법을 확인해 보세요!"
)

st.divider()

# =====================================
# 5. 근육 부위 및 검색어
# =====================================

aliases = {
    "가슴": ["가슴", "가슴근육", "흉근"],
    "등": ["등", "등근육", "광배근"],
    "어깨": ["어깨", "어깨근육", "삼각근"],
    "이두근": ["이두근", "이두", "팔 앞쪽"],
    "삼두근": ["삼두근", "삼두", "팔 뒤쪽"],
    "복부": ["복부", "복근", "배", "배근육"],
    "엉덩이": ["엉덩이", "엉덩이근육", "둔근"],
    "허벅지 앞쪽": ["허벅지 앞쪽", "허벅지 앞", "앞벅지"],
    "허벅지 뒤쪽": ["허벅지 뒤쪽", "허벅지 뒤", "햄스트링"],
    "종아리": ["종아리", "종아리근육"]
}

# =====================================
# 6. 운동 부위 입력
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

    st.session_state["selected_part"] = selected_part

    if not selected_part:

        if search_text:
            st.warning("해당 부위를 찾을 수 없습니다.")
        else:
            st.warning("운동할 부위를 입력해 주세요.")

# =====================================
# 7. 추천 가능한 운동 부위
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
# 8. 추천 운동 TOP 3
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

                plan = exercise_plan.get(row["운동명"])

                if plan:
                    st.caption(
                        f"📊 예시 운동량: "
                        f"{plan['세트']}세트 · "
                        f"{plan['횟수']}{plan['단위']}"
                    )

    # =================================
    # 9. 운동 선택
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
        # 10. 운동 상세 정보
        # =================================

        st.divider()
        st.header("📖 4. 운동 상세 정보")

        st.title(f"💪 {detail['운동명']}")

        st.info(
            f"주요 사용 근육: {detail['주요_사용_근육']}"
        )

        # 운동 추천 이유 및 난이도
        plan = exercise_plan.get(selected_exercise)

        if plan:

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "운동 난이도",
                    plan["난이도"]
                )

            with col2:
                st.metric(
                    "추천 부위",
                    part
                )

            st.success(
                f"💡 **이 운동을 추천하는 이유**\n\n"
                f"{plan['이유']}"
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

        # =================================
        # 11. 운동별 추천 운동량 및 그래프
        # =================================

        st.divider()
        st.header("📊 5. 나의 추천 운동량")

        if plan:

            set_count = plan["세트"]
            repeat_count = plan["횟수"]
            unit = plan["단위"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "추천 세트 수",
                    f"{set_count}세트"
                )

            with col2:
                st.metric(
                    "세트당 운동량",
                    f"{repeat_count}{unit}"
                )

            st.subheader("📈 세트별 운동량 그래프")

            chart_data = pd.DataFrame({
                "세트": [
                    f"{i}세트"
                    for i in range(1, set_count + 1)
                ],
                "목표 운동량": [
                    repeat_count
                    for _ in range(set_count)
                ]
            })

            st.bar_chart(
                chart_data,
                x="세트",
                y="목표 운동량",
                color="#39A7FF"
            )

            st.caption(
                f"선택한 {selected_exercise}의 "
                f"세트별 목표 운동량입니다."
            )

            st.caption(
                "※ 운동량은 초보자용 참고 예시이며 "
                "개인의 체력과 자세에 맞게 조절하세요. "
                "통증이 있으면 운동을 중단하고 지도 교사나 "
                "운동 전문가에게 자세를 확인하세요."
            )

        else:

            st.warning(
                "해당 운동의 추천 운동량 정보가 아직 없습니다."
            )

        # =================================
        # 12. 다른 운동 부위 검색
        # =================================

        st.divider()

        if st.button(
            "🔄 다른 근육 부위 검색하기",
            use_container_width=True
        ):

            st.session_state["selected_part"] = None
            st.rerun()

# =====================================
# 13. 하단 안내
# =====================================

st.divider()

st.caption(
    "FIT PICK | 근육 부위별 맞춤 운동 추천 서비스"
)

st.caption(
    "정확한 자세와 안전을 우선으로 운동하세요."
)
