
import streamlit as st
import folium
import streamlit.components.v1 as components

st.set_page_config(page_title="서울 관광 TOP 10", page_icon="📍", layout="wide")

st.title("📍 외국인 관광객이 좋아하는 서울 관광지 TOP 10")
st.caption("지도 위 번호를 누르면 관광지 이름과 설명을 확인할 수 있습니다.")

places = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "조선 왕조의 대표 궁궐로, 한국의 전통 건축과 수문장 교대식을 볼 수 있습니다."},
    {"name": "북촌한옥마을", "lat": 37.5826, "lon": 126.9830, "desc": "전통 한옥이 모여 있어 한국의 옛 주거 문화를 느낄 수 있는 마을입니다."},
    {"name": "명동", "lat": 37.5636, "lon": 126.9850, "desc": "쇼핑과 길거리 음식으로 유명하며 다양한 화장품 매장과 먹거리가 있습니다."},
    {"name": "N서울타워", "lat": 37.5512, "lon": 126.9882, "desc": "남산에 있는 전망 명소로 서울의 전경을 감상할 수 있습니다."},
    {"name": "남산공원", "lat": 37.5510, "lon": 126.9900, "desc": "서울 도심에서 자연을 즐기며 산책할 수 있는 공원입니다."},
    {"name": "인사동", "lat": 37.5740, "lon": 126.9857, "desc": "전통 공예품과 기념품 가게, 전통 찻집을 만날 수 있는 거리입니다."},
    {"name": "광장시장", "lat": 37.5701, "lon": 126.9997, "desc": "빈대떡과 김밥 등 한국의 다양한 시장 음식을 맛볼 수 있는 전통시장입니다."},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.5671, "lon": 127.0095, "desc": "독특한 건축 디자인과 전시, 패션 관련 행사를 즐길 수 있는 복합문화공간입니다."},
    {"name": "홍대거리", "lat": 37.5563, "lon": 126.9236, "desc": "개성 있는 상점과 거리 공연, 카페 등 젊은 문화를 경험할 수 있는 거리입니다."},
    {"name": "코엑스·별마당도서관", "lat": 37.5116, "lon": 127.0591, "desc": "대형 쇼핑·문화 공간으로, 높은 서가가 인상적인 별마당도서관이 유명합니다."},
]

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    control_scale=True,
    tiles="OpenStreetMap"
)

for i, place in enumerate(places, start=1):
    popup_html = (
        f"<div style='width:220px'>"
        f"<b>{i}. {place['name']}</b><br>{place['desc']}</div>"
    )

    number_icon = folium.DivIcon(
        html=(
            f"<div style='background:#e74c3c;color:white;border-radius:50%;"
            f"width:28px;height:28px;text-align:center;line-height:28px;"
            f"font-weight:bold;border:2px solid white;box-shadow:0 1px 4px #555;'>"
            f"{i}</div>"
        )
    )

    folium.Marker(
        [place["lat"], place["lon"]],
        tooltip=f"{i}. {place['name']}",
        popup=folium.Popup(popup_html, max_width=280),
        icon=number_icon
    ).add_to(m)

m.fit_bounds(
    [[p["lat"], p["lon"]] for p in places],
    padding=(25, 25)
)

# Folium 지도를 HTML로 직접 표시
components.html(
    m.get_root().render(),
    height=620,
    scrolling=False
)

st.markdown("---")
st.subheader("🌟 관광지 간단 소개")

left, right = st.columns(2)

for idx, place in enumerate(places):
    with (left if idx % 2 == 0 else right):
        st.markdown(f"**{idx + 1}. {place['name']}**")
        st.write(place["desc"])

st.caption("※ 서울의 대표 관광지를 바탕으로 구성한 추천 목록이며, 공식 실시간 인기 순위는 아닙니다.")
st.caption("※ 지도는 인터넷 연결이 필요합니다. 방문 전 운영 시간과 휴무일을 확인하세요.")
