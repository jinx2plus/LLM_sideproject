# HD-Map을 활용한 교통안전개선 LLM 개발

이 저장소는 HD-Map 기반 교통사고 노드/링크 정보를 활용해 고위험 지점을 선별하고,
LLM(대형언어모델)으로 사고 다발 구간의 교통안전 개선안을 생성/비교하는 실험 코드와 결과물을 정리한 것입니다.

## 폴더 구조

- `code/src/`: 파이썬 스크립트(주요 실행 코드)
- `code/notebooks/`: 실험 노트북
- `data/`: 입력 및 중간 산출 데이터
- `results/`: LLM 제안 결과

## 포함 파일

### `code/src/`

- `LLM241213.py`
- `LLM241213_ORIGNIAL.py`
- `LLM241214.py`
- `untitled2.py`
- `untitled3.py`

### `code/notebooks/`

- `241214_CHATGPT.ipynb`
- `241214_claude.ipynb`
- `241214_llama3.3-70b.ipynb`

### `data/`

- `TA.xlsx`
- `hd_map_data.csv`
- `high_risk_data2.csv`

### `results/`

- `safety_improvement_suggestions_END_ENGtoKOR_all_241102.csv`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241102.xlsx`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241214_chatgpt4.csv`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241214_chatgpt40.csv`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241214_gemini_pro.csv`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241214_llama33.csv`
- `safety_improvement_suggestions_END_ENGtoKOR_all_241214gemini-2.0-flash-exp.csv`

## 사용/실행 안내(요약)

1. Python 3.10+ 가상환경 생성
2. 의존성 설치 (예: `pandas`, `geopandas`, `google-generativeai`, `openai`, `scikit-learn`)
3. `data/` 경로 기준 파일 경로를 맞추거나 스크립트에서 상대 경로로 실행
4. API 호출 키는 환경변수로 주입하고, 하드코딩된 키는 삭제

## 주의사항

- 현재 스크립트 일부는 API 키가 하드코딩된 이력이 있어 GitHub 업로드 전 정리 필요
- 대용량 원시 데이터는 저장소 용량/보안 정책에 맞춰 별도 저장소 또는 공유 링크 분리 권장

## 원본 보존본

원본(마스킹 전) 소스는 다음 폴더에 보존했습니다.
- `C:\Users\jinx2\OneDrive\문서\UOS_2024\대학혁신지원사업\code_origin\`

업로드 전용 폴더(`code/`)는 API 키/토큰을 환경변수 방식으로 마스킹 처리했습니다.
