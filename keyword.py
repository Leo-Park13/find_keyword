import requests
import pandas as pd



API_KEY = "발급받은_인증키"
BASE_URL = "http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfo"

def search_bid(keyword):
    params = {
        'serviceKey': API_KEY,
        'numOfRows': '100',
        'pageNo': '1',
        'type': 'json',
        'bidNm': keyword
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

keywords = [
    "선행연구", "연구", "건축기획", "시설사업", "기본계획", "타당성(조사)",
    "세계유산", "농촌", "신활력", "도시계획", "마스터플랜", "기초생활거점조성사업", "역사문화정비"
]

results = []

for keyword in keywords:
    data = search_bid(keyword)
    # 공고 리스트를 results에 저장
    if "response" in data and "body" in data["response"]:
        items = data["response"]["body"].get("items", {}).get("item", [])
        for item in items:
            results.append(item)


for item in results:
    if item.get("prtcptLmtYn") == "Y":
        # 제한이 있는 경우만 필터링
        # 추가로 업종 코드도 확인 가능
        print(item.get("bidNtceNm"), item.get("indstrytyCdNm"))



df = pd.DataFrame(results)
df_filtered = df[df["prtcptLmtYn"] == "Y"]  # 투찰 제한 있는 공고만 필터링
df_filtered.to_excel("나라장터_투찰제한_공고.xlsx", index=False)
