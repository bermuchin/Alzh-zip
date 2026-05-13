import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import cosine # 유사도 계산용
from ai.preprocessing import load_and_preprocess, get_adjusted_mmse
from ai.image_processor import ImageFeatureExtractor

class SimilarityEngine:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. 임상 데이터 로드
        self.db = load_and_preprocess()
        self.symptom_cols = [col for col in self.db.columns if col.startswith('AX')]
        
        # 2. 이미지 추출기 및 미리 뽑아둔 특징(인덱스) 로드
        self.extractor = ImageFeatureExtractor()
        feature_path = os.path.join(BASE_DIR, 'model', 'features.npy')
        
        if os.path.exists(feature_path):
            self.db_features = np.load(feature_path)
        else:
            print("⚠️ 경고: 인덱스 파일이 없습니다. indexing.py를 먼저 실행하세요.")
            self.db_features = None

    def find_top_3_similar(self, input_data, input_img_path):
        target_df = self.db.copy()
        
        # --- [STEP 1] 임상 거리 계산 (0~1 정규화) ---
        adj_mmse = get_adjusted_mmse(input_data['MMSE_SCORE'], input_data['EDUCATION_LEVEL'])
        dist_mmse = abs(target_df['ADJUSTED_MMSE'] - adj_mmse) / 30.0
        
        symptom_values = np.array([input_data.get(col, 0) for col in self.symptom_cols])
        db_symptoms = target_df[self.symptom_cols].values
        dist_symptoms = np.sum(abs(db_symptoms - symptom_values), axis=1) / len(self.symptom_cols)
        
        dist_edu = abs(target_df['EDUCATION_LEVEL'] - input_data['EDUCATION_LEVEL']) / 2.0
        
        # 임상 종합 거리 (가중치 적용)
        clinical_score = (dist_mmse * 0.4 + dist_symptoms * 0.4 + dist_edu * 0.2)

        # --- [STEP 2] 이미지 거리 계산 (코사인 유사도) ---
        if self.db_features is not None:
            input_img_vec = self.extractor.extract(input_img_path)
            # 모든 DB 벡터와 코사인 거리 계산 (1 - cosine_similarity)
            image_scores = []
            for db_vec in self.db_features:
                # 두 벡터가 모두 0이 아닐 때만 계산
                if np.any(db_vec) and np.any(input_img_vec):
                    image_scores.append(cosine(db_vec, input_img_vec))
                else:
                    image_scores.append(1.0) # 최대 거리
            image_score = np.array(image_scores)
        else:
            image_score = np.zeros(len(target_df))

        # --- [STEP 3] 멀티모달 최종 합산 ---
        # 임상(70%) + 이미지(30%)
        target_df['similarity_score'] = (clinical_score * 0.7) + (image_score * 0.3)
        
        # --- [STEP 4] 결과 반환 ---
        top_3 = target_df.sort_values(by='similarity_score').head(3)
        return top_3.to_dict('records')