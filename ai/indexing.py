import pandas as pd
import numpy as np
import os
import torch
from tqdm import tqdm # 진행률 표시를 위해 필요
from preprocessing import load_and_preprocess
from image_processor import ImageFeatureExtractor

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_PATH = os.path.join(BASE_DIR, 'model', 'features.npy')

def create_image_index():
    # 1. 데이터 및 추출기 로드
    df = load_and_preprocess()
    extractor = ImageFeatureExtractor()
    
    features = []
    print("fMRI 이미지 특징 추출을 시작합니다...")

    # 2. 모든 행 순회하며 이미지 특징 추출
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        # CSV의 상대 경로를 절대 경로로 변환
        # 예: data/fmri_data/002_S_0295/m06.png
        img_path = os.path.join(BASE_DIR, 'data', row['LOCAL_FMRI_PATH'])
        
        if os.path.exists(img_path):
            feature = extractor.extract(img_path)
            features.append(feature)
        else:
            # 이미지가 없을 경우 0으로 채워진 벡터 삽입 (에러 방지)
            features.append(np.zeros(512))

    # 3. 넘파이 배열로 변환 후 저장
    features_array = np.array(features)
    
    if not os.path.exists(os.path.dirname(SAVE_PATH)):
        os.makedirs(os.path.dirname(SAVE_PATH))
        
    np.save(SAVE_PATH, features_array)
    print(f"인덱싱 완료! 저장 위치: {SAVE_PATH}")

if __name__ == "__main__":
    create_image_index()