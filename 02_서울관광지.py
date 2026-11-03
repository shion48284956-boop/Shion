
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 외국인 인기 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 서울 관광지 TOP 10
PLACES = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9869,
        "area": "중구",
        "description": "화장품과 패션 매장, 길거리 음식이 모여 있는 대표 쇼핑 거리입니다.",
        "reason": "외국인 방문객이 많이 찾는 서울의 대표 쇼핑 명소입니다."
    },
    {
        "rank": 2,
        "name": "남산서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "area": "용산구",
        "description": "서울의 아름다운 전경과 야경을 감상할 수 있는 전망 명소입니다.",
        "reason": "서울의 풍경을 한눈에 볼 수 있어 외국인 관광객에게 인기가 높습니다."
    },
    {
        "rank": 3,
        "name": "코엑스·별마당도서관",
        "english": "COEX & Starfield Library",
        "lat": 37.5126,
        "lon": 127.0594,
        "area": "강남구",
        "description": "쇼핑과 문화생활을 즐길 수 있으며 독특한 서가로 유명합니다.",
        "reason": "쇼핑과 사진 촬영을 함께 즐길 수 있는 인기 장소입니다."
    },
    {
        "rank": 4,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "area": "종로구",
        "description": "조선 왕조의 법궁으로 한국의 전통 건축과 역사를 경험할 수 있습니다.",
        "reason": "한국의 역사와 전통문화를 체험할 수 있는 대표 관광지입니다."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "area": "마포구",
        "description": "거리 공연과 음악, 개성 있는 상점과 카페가 모여 있습니다.",
        "reason": "젊은 문화와 다양한 볼거리를 경험할 수 있습니다."
    },
    {
        "rank": 6,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "area": "종로구",
        "description": "전통 한옥이 모여 있어 한국의 옛 주거 문화를 살펴볼 수 있습니다.",
        "reason": "한국 전통 건축과 분위기를 경험하고 싶은 관광객에게 인기입니다."
    },
    {
        "rank": 7,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "area": "종로구",
        "description": "빈대떡과 마약김밥 등 다양한 한국 길거리 음식을 맛볼 수 있습니다.",
        "reason": "한국의 전통시장과 먹거리를 체험할 수 있습니다."
    },
    {
        "rank": 8,
        "name": "동대문디자인플라자",
        "english": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "area": "중구",
        "description": "독특한 곡선형 건축물과 전시, 디자인 행사를 만날 수 있습니다.",
        "reason": "건축물과 문화 행사를 즐길 수 있는 복합문화공간입니다."
    },
    {
        "rank": 9,
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0560,
        "area": "성동구",
        "description": "개성 있는 카페와 편집숍, 팝업스토어가 모여 있는 거리입니다.",
        "reason": "서울의 최신 유행과 독특한 카페 문화를 경험할 수 있습니다."
    },
    {
        "rank": 10,
        "name": "강남역 일대",
        "english": "Gangnam",
        "lat": 37.4979,
        "lon": 127.0276,
        "area": "강남구",
        "description": "쇼핑과 음식점, 뷰티·패션 매장이 밀집한 번화가입니다.",
        "reason": "서울의 현대적인 도시 분위기를 느낄 수 있습니다."
    }
]

# 제목
st.title("🗺️ 외국인 관광객이 좋아하는 서울 TOP 10")
st.write(
    "서울을 방문하는 외국인 관광객을 위한 "
    "대표 관광지를 지도에서 확인해 보세요!"
)

st.info(
    "※ 외국인 관광객 방문 자료와 관광지 선호 정보를 "
    "바탕으로 구성한 추천 목록이며, 공식 단일 순위는 아닙니다."
)

# 지도 만들기
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커 표시
for place in PLACES:

    popup_html = f"""
    <div style="width:210px">
        <h4>{place['rank']}. {place['name']}</h4>
        <p>{place['english']}</p>
        <p>{place['description']}</p>
    </div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}. {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=260
        ),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#2563eb;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                font-size:13px;
                box-shadow:0 1px 5px rgba(0,0,0,.35);
            ">
                {place['rank']}
            </div>
            """,
            icon_size=(30, 30),
            icon_anchor=(15, 15)
        )
    ).add_to(m)

# 화면에 지도 출력
st_folium(
    m,
    use_container_width=True,
    height=570,
    returned_objects=[]
)

# 관광지 설명
st.subheader("📍 서울 관광지 TOP 10 소개")

for place in PLACES:

    with st.container(border=True):

        st.markdown(
            f"### {place['rank']}. {place['name']}"
        )

        st.caption(
            f"{place['english']} | {place['area']}"
        )

        st.write(place["description"])

        st.info(
            f"⭐ 인기 이유: {place['reason']}"
        )

# 참고 자료
st.divider()

st.subheader("📚 참고 자료")

st.markdown("""
- [서울 공식 관광정보](https://english.visitseoul.net/)
- [한국관광공사](https://english.visitkorea.or.kr/)
- [서울시 관광정보](https://english.seoul.go.kr/)
""")

st.caption(
    "지도 제공: OpenStreetMap | "
    "관광지 위치는 대표 좌표를 사용합니다."
)
