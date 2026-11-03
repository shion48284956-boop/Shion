
import streamlit as st

st.set_page_config(
    page_title="서울 관광 가이드",
    page_icon="🇰🇷",
    layout="wide"
)

st.title("🇰🇷 서울 관광 가이드")
st.subheader("외국인 관광객을 위한 서울 여행 정보")

st.markdown("""
서울의 다양한 관광지를 알아보고
한국의 문화와 음식, 아름다운 풍경을 경험해 보세요!
""")

st.info("왼쪽 메뉴에서 서울 관광지 TOP 10을 선택해 주세요.")

st.markdown("### 🗺️ 서울 여행의 매력")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏯")
    st.write("한국 전통문화")

with col2:
    st.markdown("### 🍜")
    st.write("다양한 한국 음식")

with col3:
    st.markdown("### 🌆")
    st.write("아름다운 서울의 풍경")

st.divider()

st.markdown("### ✈️ 추천 여행")
st.write(
    "경복궁에서 한국의 역사를 알아보고, "
    "광장시장에서 한국 음식을 맛본 뒤 "
    "남산서울타워에서 서울의 야경을 감상해 보세요!"
)

st.caption("Seoul Travel Guide")
