import os
from ai.similarity import SimilarityEngine

def test_recommendation():
    # 1. 엔진 초기화
    print("엔진 초기화 중입니다...")
    engine = SimilarityEngine()
    
    # 2. 테스트용 입력 데이터 설정
    # (실제 서비스에서는 Streamlit UI를 통해 들어올 데이터입니다)
    test_input_data = {
        'EDUCATION_LEVEL': 2,      # 대졸 이상
        'MMSE_SCORE': 24,         # 인지 점수
        # 주요 증상 설정 (1: 있음, 0: 없음)
        'AXDIARRH': 1, 
        'AXCONSTP': 1,
        'AXVISION': 1,
        # 나머지 증상은 일단 0으로 가정 (엔진 내부에서 처리됨)
    }
    
    # 3. 테스트용 이미지 경로 
    # (data/fmri_data 폴더 안에 있는 실제 파일 하나를 지정해보세요)
    # 예: "data/fmri_data/002_S_0295/m06.png"
    sample_img_path = os.path.join("data", "fmri_data", "002_S_0295", "m06.png")
    
    if not os.path.exists(sample_img_path):
        print(f"테스트용 이미지가 없습니다: {sample_img_path}")
        print("실제 존재하는 이미지 경로로 수정 후 다시 시도해주세요.")
        return

    # 4. 유사 환자 검색 실행
    print("유사한 환자 top 3 찾는 중...")
    recommendations = engine.find_top_3_similar(test_input_data, sample_img_path)
    
    # 5. 결과 출력
    print("\n" + "="*50)
    print("🎯 [검사 결과] 유사 사례 Top 3 추천")
    print("="*50)
    
    for i, res in enumerate(recommendations):
        summary = res['summary']
        
        print(f"\n[{i+1}순위 유사 환자]")
        print(f" - 환자 ID: {summary['ptid']}")
        print(f" - 방문 시점: {summary['matched_month']}개월 차")
        print(f" - 유사도 점수: {summary['similarity']}% (높을수록 유사)")
        print(f" - 보정 MMSE: {summary['mmse']}")
        
        # 상세 데이터 포함 여부 확인 (테스트용)
        print(f" - 공통 증상: {', '.join(res['symptoms']['common'])}")
        print(f" - fMRI 시퀀스: {len(res['fmri_display']['sequence']['paths'])}장 확보됨")
        
    print("\n" + "="*50)

if __name__ == "__main__":
    test_recommendation()