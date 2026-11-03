
import streamlit as st
import folium
import streamlit.components.v1 as components

st.set_page_config(
    page_title="서울 관광 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인 관광객을 위한 서울 관광 TOP 10")
st.write("서울의 대표 관광지를 지도와 함께 살펴보세요!")
st.caption("외국인 관광객에게 소개하기 좋은 서울의 대표 명소 10곳입니다.")

# 관광지 정보
places = [
    {
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 시대 대표 궁궐입니다. 한국의 전통 건축과 수문장 교대식을 볼 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥이 모여 있는 마을로 한국의 옛 주거 문화를 느낄 수 있습니다."
    },
    {
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9850,
        "desc": "쇼핑과 길거리 음식, 다양한 화장품 매장으로 유명한 거리입니다."
    },
    {
        "name": "N서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "남산에 있는 전망 명소로 서울의 아름다운 전경을 감상할 수 있습니다."
    },
    {
        "name": "인사동",
        "lat": 37.5740,
        "lon": 126.9857,
        "desc": "전통 공예품과 기념품 가게, 전통 찻집을 만날 수 있는 문화 거리입니다."
    },
    {
        "name": "광장시장",
        "lat": 37.5701,
        "lon": 126.9997,
        "desc": "빈대떡과 김밥 등 한국의 다양한 시장 음식을 맛볼 수 있는 전통시장입니다."
    },
    {
        "name": "동대문디자인플라자",
        "lat": 37.5671,
        "lon": 127.0095,
        "desc": "독특한 건축 디자인과 전시, 패션 행사를 즐길 수 있는 복합문화공간입니다."
    },
    {
        "name": "홍대거리",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "개성 있는 상점과 카페, 거리 공연 등 젊은 문화를 경험할 수 있습니다."
    },
    {
        "name": "코엑스·별마당도서관",
        "lat": 37.5116,
        "lon": 127.0591,
        "desc": "대형 쇼핑·문화 공간으로 높은 서가가 인상적인 별마당도서관이 유명합니다."
    },
    {
        "name": "청계천",
        "lat": 37.5692,
        "lon": 126.9788,
        "desc": "서울 도심을 따라 흐르는 하천 산책로로 여유롭게 산책하기 좋은 장소입니다."
    }
]

# 서울 지도 만들기
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 지도에 관광지 표시
for number, place in enumerate(places, start=1):

    popup_text = f"""
    <b>{number}. {place['name']}</b><br>
    {place['desc']}
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{number}. {place['name']}",
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color:#e74c3c;
                color:white;
                border-radius:50%;
                width:30px;
                height:30px;
                text-align:center;
                line-height:30px;
                font-weight:bold;
                border:2px solid white;">
                {number}
            </div>
            """
        )
    ).add_to(m)

# 모든 관광지가 보이도록 지도 범위 설정
m.fit_bounds([
    [place["lat"], place["lon"]]
    for place in places
])

# 지도 화면에 표시
components.html(
    m.get_root().render(),
    height=620,
    scrolling=False
)

# 지도 아래 관광지 설명
st.divider()
st.subheader("📍 서울 관광지 TOP 10 소개")

left, right = st.columns(2)

for index, place in enumerate(places):
    with (left if index % 2 == 0 else right):
        st.markdown(f"### {index + 1}. {place['name']}")
        st.write(place["desc"])

st.divider()
st.caption("※ 공식 실시간 인기 순위가 아닌 서울 대표 관광지 추천 목록입니다.")
st.caption("※ 지도 표시에는 인터넷 연결이 필요합니다.")
