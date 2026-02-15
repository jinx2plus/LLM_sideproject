# -*- coding: utf-8 -*-
import os
import pandas as pd
import google.generativeai as genai


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")

genai.configure(api_key=GOOGLE_API_KEY)


def mode_or_default(series, default="미확인"):
    non_null = series.dropna()
    if len(non_null) == 0:
        return default
    modes = non_null.mode()
    if len(modes) == 0:
        return default
    return modes.iloc[0]


def build_prompt(row):
    return f"""당신은 교통안전 전문가입니다.
다음은 링크 단위 사고 요약입니다.
LINK_ID: {row['LINK_ID']}
연결 노드: {row['NODE_IDS']}
사고 건수: {row['total_accidents']}
사망자: {row['total_deaths']}
중상자: {row['total_serious_injuries']}
사고유형: {row['Crashtype']}
도로 특성: MAX_SPD={row['MAX_SPD']}, LANES={row['LANES']}, ROAD_TYPE={row['ROAD_TYPE']}, NODE_TYPE={row['NODE_TYPE']}, TURN_P={row['TURN_P']}
이 링크의 교통안전 개선 대안을 한국어로 5개 항목으로 제시해 주세요."""


def generate_safety_improvement_suggestion(row, model):
    try:
        response = model.generate_content(build_prompt(row))
        return response.text.strip()
    except Exception as e:
        print(f"[LLM ERROR] LINK_ID={row['LINK_ID']} {e}")
        return f"[LLM 생성 실패] {e}"


file_path = r"TA.xlsx"
data = pd.read_excel(file_path)

high_risk_areas = data.groupby("LINK_ID").agg(
    NODE_IDS=("NODE_ID", lambda s: ",".join(dict.fromkeys(s.dropna().astype(str))),
    total_accidents=("NO", "count"),
    total_deaths=("Deaths", "sum"),
    total_serious_injuries=("SeriousInj", "sum"),
    total_injuries=("InjNO", "sum"),
    Crashtype=("Crashtype", mode_or_default),
    Weather=("Weather", mode_or_default),
    NODE_TYPE=("NODE_TYPE", mode_or_default),
    TURN_P=("TURN_P", mode_or_default),
    LANES=("LANES", mode_or_default),
    ROAD_TYPE=("ROAD_TYPE", mode_or_default),
    CONNECT=("CONNECT", mode_or_default),
    MAX_SPD=("MAX_SPD", mode_or_default),
    REST_VEH=("REST_VEH", mode_or_default),
    CURVATURE=("CURVATURE", mode_or_default),
    SLOPE=("SLOPE", mode_or_default),
).reset_index()

high_risk_areas = high_risk_areas[
    (high_risk_areas["total_accidents"] > 5)
    | (high_risk_areas["total_deaths"] > 0)
    | (high_risk_areas["total_serious_injuries"] > 2)
]

model = genai.GenerativeModel("gemini-2.0-flash-exp")
high_risk_areas["safety_suggestion"] = high_risk_areas.apply(
    lambda row: generate_safety_improvement_suggestion(row, model), axis=1
)

high_risk_areas[
    [
        "LINK_ID",
        "NODE_IDS",
        "total_accidents",
        "total_deaths",
        "total_serious_injuries",
        "Crashtype",
        "Weather",
        "NODE_TYPE",
        "TURN_P",
        "LANES",
        "ROAD_TYPE",
        "CONNECT",
        "MAX_SPD",
        "REST_VEH",
        "CURVATURE",
        "SLOPE",
        "safety_suggestion",
    ]
].to_csv(
    "safety_improvement_suggestions_END_ENGtoKOR_all_241213.csv",
    index=False,
    encoding="utf-8-sig",
)

print(high_risk_areas[["LINK_ID", "safety_suggestion"]].head())
