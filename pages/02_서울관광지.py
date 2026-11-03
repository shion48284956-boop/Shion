
import streamlit as st
import folium
import streamlit.components.v1 as components

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인 관광객이 좋아하는 서울 TOP 10")
st.write("서울의 대표 관광지를 지도에서 확인해 보세요!")

st.info(
    "외국인 관광객의 방문 및 선호 정보를 참고해 구성한 "
    "서울의 대표 관광지 추천 목록입니다."
)

# -----------------------------
# 관광지 데이터
# -----------------------------
places = [
    {
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9869,
        "area": "중구",
        "description": "화장품, 패션 매장과 다양한 길거리 음식이 유명한 쇼핑 거리입니다.",
        "reason": "쇼핑과 한국 길거리 음식을 즐길 수 있습니다."
    },
    {
        "name": "남산서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "area": "용산구",
        "description": "서울의 아름다운 전경과 야경을 감상할 수 있는 전망 명소입니다.",
        "reason": "서울의 풍경을 한눈에 볼 수 있습니다."
    },
    {
        "name": "코엑스·별마당도서관",
        "english": "COEX Starfield Library",
        "lat": 37.5126,
        "lon": 127.0594,
        "area": "강남구",
        "description": "독특한 서가와 다양한 쇼핑 공간을 즐길 수 있습니다.",
        "reason": "쇼핑과 사진 촬영을 함께 즐길 수 있습니다."
    },
    {
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "area": "종로구",
        "description": "조선 왕조의 대표 궁궐로 한국의 전통 건축과 역사를 경험할 수 있습니다.",
        "reason": "한국의 역사와 전통문화를 체험할 수 있습니다."
    },
    {
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "area": "마포구",
        "description": "거리 공연과 음악, 개성 있는 카페와 상점이 모여 있습니다.",
        "reason": "젊은 문화와 다양한 볼거리를 즐길 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "area": "종로구",
        "description": "전통 한옥이 모여 있는 한국의 대표적인 전통 마을입니다.",
        "reason": "한국의 옛 주거문화와 건축을 경험할 수 있습니다."
    },
    {
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "area": "종로구",
        "description": "빈대떡과 김밥 등 다양한 한국 전통 음식을 맛볼 수 있습니다.",
        "reason": "한국의 전통시장과 먹거리를 경험할 수 있습니다."
    },
    {
        "name": "동대문디자인플라자",
        "english": "DDP",
        "lat": 37.5671,
        "lon": 127.0095,
        "area": "중구",
        "description": "독특한 건축 디자인과 다양한 전시를 즐길 수 있습니다.",
        "reason": "현대적인 건축물과 문화행사를 경험할 수 있습니다."
    },
    {
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0560,
        "area": "성동구",
        "description": "개성 있는 카페와 편집숍, 팝업스토어가 모여 있습니다.",
        "reason": "서울의 최신 유행과 카페 문화를 경험할 수 있습니다."
    },
    {
        "name": "강남역 일대",
        "english": "Gangnam",
        "lat": 37.4979,
        "lon": 127.0276,
        "area": "강남구",
        "description": "쇼핑과 음식점, 뷰티 매장이 밀집한 번화가입니다.",
        "reason": "서울의 현대적인 도시 분위기를 느낄 수 있습니다."
    }
]

# -----------------------------
# Folium 지도 생성
# -----------------------------
st.subheader("📍 서울 관광지 지도")

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap",
    width="100%",
    height="100%"
)

# 관광지 마커 생성
for number, place in enumerate(places, start=1):

    popup_html = f"""
    <div style="width:230px; font-family:sans-serif;">
        <h3>{number}. {place['name']}</h3>
        <p><b>{place['english']}</b></p>
        <p>{place['description']}</p>
        <p>📍 {place['area']}</p>
    </div>
    """

    folium.Marker(
        location=[
            place["lat"],
            place["lon"]
        ],
        tooltip=f"{number}. {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color:#2563eb;
                color:white;
                width:34px;
                height:34px;
                border-radius:50%;
                border:2px solid white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                font-size:14px;
                box-shadow:0 2px 6px rgba(0,0,0,0.4);
            ">
                {number}
            </div>
            """,
            icon_size=(34, 34),
            icon_anchor=(17, 17)
        )
    ).add_to(m)

# 관광지 10곳이 한 화면에 보이도록 설정
coordinates = [
    [place["lat"], place["lon"]]
    for place in places
]

m.fit_bounds(
    coordinates,
    padding=[30, 30]
)

# -----------------------------
# 지도 화면 출력
# -----------------------------
map_html = m.get_root().render()

components.html(
    map_html,
    height=650,
    scrolling=False
)

st.caption(
    "지도의 번호를 클릭하면 관광지 정보를 확인할 수 있습니다."
)

# -----------------------------
# 관광지 설명
# -----------------------------
st.divider()

st.header("🏙️ 서울 관광지 TOP 10 소개")

for number, place in enumerate(places, start=1):

    with st.container(border=True):

        st.subheader(
            f"{number}. {place['name']}"
        )

        st.caption(
            f"{place['english']} | {place['area']}"
        )

        st.write(place["description"])

        st.success(
            "⭐ 인기 포인트: " + place["reason"]
        )

# -----------------------------
# 참고 자료
# -----------------------------
st.divider()

st.subheader("📚 참고 사이트")

st.markdown("""
- [서울 공식 관광정보](https://english.visitseoul.net/)
- [한국관광공사](https://english.visitkorea.or.kr/)
- [서울시 공식 홈페이지](https://english.seoul.go.kr/)
""")

st.caption("Map powered by Folium & OpenStreetMap")
