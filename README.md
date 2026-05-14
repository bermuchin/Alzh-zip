# 알집 Alz' Zip

알집(Alz' Zip)은 알츠하이머 진단 지원을 위한 Streamlit 기반 웹 프로토타입입니다. 의료진이 환자 프로필을 관리하고, MMSE 점수·증상 체크리스트·fMRI 이미지를 입력하면 기존 환자 데이터베이스에서 유사 사례 Top 3를 찾아 상세 리포트로 제공합니다.

## 주요 기능

### 의료진 인증 및 워크스페이스

- 의료진 로그인 화면 제공
- 의료진 코드 승인 후 계정 생성 흐름 제공
- 로그인 이후 좌측 내비게이션 기반 환자 워크스페이스 제공

### 환자 프로필 관리

- 등록 환자 목록 조회
- 환자 이름 검색 및 이름·생년월일·성별 기준 정렬
- 환자 프로필 추가, 수정, 삭제
- 환자 상세 정보 조회
- 환자별 AI 진단 이력 저장 및 재조회

### AI 유사 사례 매칭

- MMSE 점수 입력
- 증상 체크박스 입력
- fMRI 이미지 업로드
- 임상 데이터와 이미지 특징을 결합한 유사 환자 Top 3 추천
- 유사도, 매칭 시점, 보정 MMSE, 공통 증상 요약 제공
- 상세 리포트에서 다음 정보를 시각적으로 확인
  - 입력 환자와 유사 환자의 기본 정보 비교
  - 공통 증상 및 전체 증상 비교
  - 유사 환자의 MMSE 변화 추이
  - 입력 fMRI와 유사 환자의 fMRI 시퀀스 비교

## AI 매칭 로직 개요

현재 AI 엔진은 `ai/` 디렉토리의 모듈로 구성되어 있습니다.

1. `preprocessing.py`
   - 환자 CSV 데이터 로드
   - fMRI 이미지 경로 정규화
   - 방문 시점(`VISCODE`, `VISDATE`)을 월 단위(`MONTHS`)로 변환
   - 학력 수준에 따른 MMSE 보정
   - 증상 컬럼(`AX*`)을 매칭 가능한 이진 값으로 변환

2. `image_processor.py`
   - Torchvision ResNet18 사전학습 모델 로드
   - 마지막 분류 레이어를 제거해 512차원 이미지 특징 벡터 추출

3. `indexing.py`
   - 내부 fMRI 이미지 전체를 순회하며 특징 벡터를 생성
   - 생성 결과를 `model/features.npy`로 저장

4. `similarity.py`
   - 입력 환자의 MMSE, 증상, 학력 정보를 기존 환자 데이터와 비교
   - 업로드된 fMRI 이미지와 사전 생성된 이미지 특징 벡터를 코사인 거리로 비교
   - 임상 거리 70%, 이미지 거리 30% 가중치로 최종 유사도 산출
   - 유사 환자 Top 3를 반환

5. `postprocessing.py`
   - 프론트엔드 상세 리포트에 필요한 형태로 결과를 가공
   - 유사 환자의 과거 MMSE 이력, fMRI 시퀀스, 공통 증상 정보를 패키징

## 프로젝트 구조

```text
.
├── app.py                         # Streamlit 메인 애플리케이션
├── requirements.txt               # Python 의존성 목록
├── test_similarity.py             # SimilarityEngine 로컬 테스트 스크립트
├── ai/
│   ├── preprocessing.py           # 데이터 로드 및 전처리
│   ├── image_processor.py         # fMRI 이미지 특징 추출
│   ├── indexing.py                # 이미지 특징 인덱스 생성
│   ├── similarity.py              # 유사 환자 매칭 엔진
│   └── postprocessing.py          # 상세 리포트용 결과 후처리
├── assets/
│   ├── logo_remove.png            # 서비스 로고
│   ├── ch_design.jpg              # UI/브랜딩 이미지
│   └── ch_view_design.jpg         # UI/브랜딩 이미지
├── model/
│   └── features.npy               # 비공개 이미지 특징 인덱스, GitHub 미포함
└── data/                          # 비공개 임상/fMRI 데이터, GitHub 미포함
    ├── ADSXLIST_final_with_paths.csv
    └── fmri_data/
```

## 비공개 데이터 및 GitHub 업로드 정책

다음 파일과 디렉토리는 내부 데이터이므로 GitHub 저장소에 포함하지 않습니다.

```text
data/
model/features.npy
```

`.gitignore`에는 다음 항목이 포함되어 있어야 합니다.

```gitignore
data/
fMRI_data/
model/*.npy
```

공개 저장소를 클론한 사용자에게는 UI 코드와 AI 엔진 구조만 제공됩니다. 실제 AI 진단 실행을 위해서는 아래 로컬 자산을 별도로 준비해야 합니다.

```text
data/ADSXLIST_final_with_paths.csv
model/features.npy
```

또한 CSV 안의 `LOCAL_FMRI_PATH` 값이 실제 로컬 fMRI 이미지 경로와 연결되어야 합니다.

## 기술 스택

- Python 3.13
- Streamlit
- Pandas
- NumPy
- SciPy
- PyTorch
- Torchvision
- Pillow
- tqdm

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd <project-directory>
```

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

```bash
pip install -r requirements.txt
```

PyTorch 설치가 환경에 따라 실패하는 경우, CPU/GPU 및 운영체제에 맞는 PyTorch 설치 명령을 먼저 적용한 뒤 나머지 패키지를 설치하세요.

## 실행 방법

### UI 실행

```bash
streamlit run app.py
```

환자 목록, 프로필 추가/수정/삭제, 로그인/회원가입 UI는 공개 코드만으로 확인할 수 있습니다. AI 진단 실행은 비공개 `data/`와 `model/features.npy`가 준비되어 있어야 정상 동작합니다.

### 이미지 특징 인덱스 생성

`model/features.npy`가 없는 로컬 환경에서는 내부 데이터가 준비된 상태에서 인덱스를 생성합니다.

```bash
python ai/indexing.py
```

이 명령은 `data/ADSXLIST_final_with_paths.csv`를 읽고, CSV에 연결된 fMRI 이미지를 순회하며 ResNet18 기반 특징 벡터를 생성한 뒤 `model/features.npy`에 저장합니다.

### 유사도 엔진 테스트

내부 데이터와 샘플 fMRI 이미지가 있는 환경에서 다음 테스트 스크립트를 실행할 수 있습니다.

```bash
python test_similarity.py
```

테스트 이미지 경로는 `test_similarity.py` 안의 `sample_img_path` 값을 실제 존재하는 fMRI 이미지 경로로 수정해 사용합니다.

## 사용 흐름

1. 의료진 계정으로 로그인합니다.
2. 환자 목록에서 기존 환자를 선택하거나 새 환자 프로필을 추가합니다.
3. `AI 진단` 화면에서 MMSE 점수, 증상, fMRI 이미지를 입력합니다.
4. `진단 실행` 버튼을 누르면 유사 환자 Top 3 결과가 생성됩니다.
5. 결과 카드를 선택하면 상세 리포트에서 증상 비교, MMSE 추이, fMRI 시퀀스를 확인할 수 있습니다.
6. 실행 결과는 해당 환자의 진단 이력에 저장되며 환자 상세 화면에서 다시 확인할 수 있습니다.

## 참고 사항 및 제한 사항

- `data/` 디렉토리와 `model/features.npy`가 없는 공개 저장소 환경에서는 AI 진단 실행이 제한됩니다.
- Torchvision의 ResNet18 사전학습 가중치는 최초 실행 시 로컬 캐시에 없으면 다운로드가 필요할 수 있습니다.