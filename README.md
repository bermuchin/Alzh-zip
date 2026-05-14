# 알집 Alz' Zip

AI 기반 알츠하이머 진단 지원을 위한 Streamlit 프로토타입입니다. 의료진 로그인, 환자 프로필 관리, 증상 및 fMRI 이미지 입력, 유사 환자군 매칭 결과 확인 흐름을 하나의 웹 앱에서 제공합니다.

## 주요 기능

- 의료진 로그인 및 계정 생성 화면
- 환자 목록 조회, 검색, 정렬
- 환자 프로필 추가, 수정, 삭제
- 환자 상세 정보 및 과거 진단 이력 조회
- 증상 체크박스와 fMRI 이미지 업로드 기반 AI 진단 지원 화면
- 유사 환자 매칭 결과 카드 및 세부 정보 표시
- Streamlit session state 기반 데모 데이터 관리

## 프로젝트 구조

```text
.
├── app.py                    # Streamlit 메인 애플리케이션
├── requirements.txt
├── ai/
│   ├── similarity.py                    
│   ├── preprocessing.py
│   ├── image_processor.py
│   ├── indexing.py
│   └── postprocessing.py
├── model/
│   └── features.npy
├── data/
│   ├── ADSXLIST_final_with_paths.csv
│   └── fmri_data/
└── assets/
    ├── logo_remove.png
    ├── ch_design.jpg
    └── ch_view_design.jpg
```

## 기술 스택

### Frontend & Web Framework
- Python 3.13+: 메인 개발 언어
- Streamlit: 데이터 사이언스 기반 대화형 웹 애플리케이션 프레임워크
- HTML5 / CSS3: 의료용 대시보드 구현을 위한 커스텀 스타일링 및 컴포넌트 디자인

### AI Engine & Deep Learning
- PyTorch: 딥러닝 모델 구현 및 연산
- Torchvision (ResNet18): 사전 학습된 신경망을 이용한 fMRI 이미지 특징 추출(Feature Extraction)
- Pillow (PIL): 의료용 이미지 데이터 로딩 및 전처리

### Data Analysis & Processing
- Pandas: 환자 임상 데이터(CSV) 핸들링 및 전처리
- NumPy: 벡터 연산 및 이미지 특징 벡터 데이터 처리
- Custom Preprocessing: 학력 수준에 따른 MMSE 점수 보정 알고리즘 및 시계열(MONTHS) 정규화 로직

### Algorithms & Logic
- Multi-modal Fusion: 임상 데이터(70%)와 이미지 데이터(30%)를 결합한 환자 유사도 점수 산출 로직
- Cosine Similarity: 이미지 특징 벡터 간의 구조적 유사성 비교
- Time-series Analysis: 유사 환자의 과거 방문 이력 기반 인지 저하 추이 시각화

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
