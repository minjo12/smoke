import folium
from folium.plugins import MarkerCluster as MC
from folium.plugins import Fullscreen, Search
import pandas as pd
import json


def show_smoking():
    # CSV 파일을 읽어와 데이터프레임(sd)로 저장 (UTF-8 인코딩, 쉼표로 구분된 파일)
    sd = pd.read_csv('./static/smoking.csv', encoding='utf-8', sep=',')

    # '위도'와 '경도' 열에 결측값(NaN)이 있는 행을 제거
    sd = sd.dropna(subset=['위도', '경도'])

    # 서울시 군(구)별 GeoJSON 파일을 불러옴 (지역 경계 데이터)
    seoul_gun = json.load(open('./static/seoul_gun.json', encoding='utf-8'))

    # 지도 객체 생성 (중심 좌표: 서울 시청, 줌 레벨: 11)
    map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 반응형 스타일을 적용하여 사용자 디스플레이에 적응 및 상단 바 추가
    map.get_root().html.add_child(folium.Element("""
        <style>
            #map { height: calc(100vh - 100px); }
        </style>
        <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        line-height: 50px;
        font-size: 20px;
        z-index: 1000;">
        <b>smoke.py</b>
        </div>
    """))

    # GeoJSON 데이터를 지도 위에 표시 (서울 군별 경계선 스타일 적용)
    geojson_layer = folium.GeoJson(
        seoul_gun,
        style_function=lambda x: {
            'fillColor': 'blue',  # 채우기 색상: 파란색
            'color': 'black',     # 경계선 색상: 검정색
            'weight': 2,          # 경계선 두께: 2
            'fillOpacity': 0.1    # 채우기 투명도: 10%
        }
    ).add_to(map)  # 지도에 추가

    # 마커 클러스터링 객체 생성 (마커를 그룹화하여 지도 혼잡도를 줄임)
    mc = MC().add_to(map)

    # Fullscreen 플러그인 추가
    fullscreen = Fullscreen(position="bottomright", title="Expand Map", title_cancel="Exit Fullscreen")
    fullscreen.add_to(map)

    # 데이터프레임의 각 행을 반복 처리
    for i, r in sd.iterrows():
        # 현재 행에서 데이터를 읽어옴
        nm = r['시설형태']   # 시설 형태
        ad = r['설치 위치']  # 설치 위치
        te = r['데이터기준일']  # 데이터 기준일
        lo = r['위도']        # 위도
        la = r['경도']        # 경도

        # 팝업에 표시할 HTML 내용 생성
        ps = f'<b>시설형태:{nm}</b><br>설치 위치:{ad}<br>데이터기준일:{te}<br>'
        # 커스텀 아이콘 설정
        custom_icon = folium.CustomIcon(
            "static/smoking_area.png",
            icon_size=(50, 50)
        )
        # 지도에 추가할 마커 생성 (위도, 경도로 위치 지정)
        mk = folium.Marker(
            [lo, la],  # 마커 위치
            popup=folium.Popup(ps, max_width=400),  # 팝업 내용 및 최대 너비 설정
            icon=custom_icon,
        )

        # 마커를 클러스터에 추가
        mk.add_to(mc)

    search = Search(
        layer=geojson_layer,
        search_label="name",
        placeholder="ex) 강남구, 종로구 ...",
        collapsed=False,
        geom_type="Polygon",
        position="bottomleft",
    ).add_to(map)

    # 지도 HTML 렌더링하여 반환 (Flask 뷰에서 사용)
    return map.get_root().render()
