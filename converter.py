import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# 함수: 주소를 위도와 경도로 변환
def get_lat_lon(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        time.sleep(1)  # Timeout 발생 시 1초 대기 후 재시도
        return get_lat_lon(address)

# Geolocator 초기화
geolocator = Nominatim(user_agent="geoapi_exercise")

# CSV 파일 읽기
file_path = r"C:\Users\82104\Downloads\서울특별시_중랑구_흡연시설_20240419.csv" # 여기에 파일 경로 입력
data = pd.read_csv(file_path, encoding='euc-kr')

# 결과 열 추가
data["위도"] = None
data["경도"] = None

# 주소 열 지정 (예: '설치 위치' 열이 주소를 포함)
address_column = "주소"

# 각 주소에 대해 위도와 경도 변환
for idx, row in data.iterrows():
    address = row[address_column]
    lat, lon = get_lat_lon(address)
    data.at[idx, "위도"] = lat
    data.at[idx, "경도"] = lon
    print(f"Processed {idx+1}/{len(data)}: {address} -> {lat}, {lon}")

# 새로운 CSV 파일로 저장
output_path = "output_with_coordinates.csv"
data.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"새 파일이 저장되었습니다: {output_path}")
