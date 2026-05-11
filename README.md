# 알집 Alz' Zip

AI 기반 알츠하이머 진단 지원을 위한 Streamlit 프로토타입입니다. 의료진 로그인, 환자 프로필 관리, 증상 및 fMRI 이미지 입력, 유사 환자군 매칭 결과 확인 흐름을 하나의 웹 앱에서 제공합니다.

## 주요 기능

- 의료진 로그인 및 계정 생성 화면
- 환자 목록 조회, 검색, 정렬
- 환자 프로필 추가, 수정, 삭제
- 환자 상세 정보 및 과거 진단 이력 조회
- 증상 체크박스와 fMRI 이미지 업로드 기반 AI 진단 지원 화면
- mock 유사 환자 매칭 결과 카드 및 표 형태 표시
- Streamlit session state 기반 데모 데이터 관리

## 프로젝트 구조

```text
.
├── app.py                    # Streamlit 메인 애플리케이션
├── requirements.txt          # Python 의존성 목록, 현재 비어 있음 (추가 필요)
├── ai/ # 향후 기능 추가 예정
│   ├── __init__.py           
│   ├── predictor.py          
│   ├── preprocessing.py
│   └── postprocessing.py
├── models/  # 향후 기능 추가 예정
└── assets/
    ├── logo_remove.png
    ├── ch_design.jpg
    └── ch_view_design.jpg
```

## 기술 스택

- Python
- Streamlit
- pandas
- HTML/CSS 커스텀 스타일링
-  ...
- 이후 추가 예정

## 설치 및 실행 방법

### 1. 저장소 준비

```bash
git clone <repository-url>
cd <project-directory>
```

압축 파일로 전달받은 경우에는 압축을 해제한 뒤 프로젝트 루트 디렉터리로 이동합니다.

### 2. 가상환경 생성 및 활성화

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. 의존성 설치

`requirements.txt` 작성 전 (구현 완료 전)

```bash
pip install streamlit pandas
```

`requirements.txt` 작성 후 (구현 후)

```text
streamlit
pandas
```

```bash
pip install -r requirements.txt
```

### 4. 앱 실행

```bash
streamlit run app.py
```
