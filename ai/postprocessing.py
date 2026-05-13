import pandas as pd
import numpy as np
import os
from ai.preprocessing import get_adjusted_mmse

class PostProcessor:
    def __init__(self, full_db):
        # 전체 데이터베이스를 들고 있어야 특정 환자의 과거 이력(MMSE 추이 등)을 찾을 수 있습니다.
        self.db = full_db
        self.symptom_cols = [col for col in self.db.columns if col.startswith('AX')]

    def get_patient_history(self, ptid):
        """특정 환자의 전체 방문 이력(MMSE 추이) 추출"""
        history = self.db[self.db['PTID'] == ptid].sort_values('MONTHS')
        return history[['MONTHS', 'ADJUSTED_MMSE']].to_dict('records')

    def get_fmri_sequence(self, ptid, current_months, count=5):
        """유사 환자의 매칭 시점 전후 fMRI 사진 경로 추출 (3~5장)"""
        # 해당 환자의 모든 fMRI 기록
        patient_imgs = self.db[self.db['PTID'] == ptid].sort_values('MONTHS')
        
        # 현재 매칭된 시점의 인덱스 찾기
        idx = patient_imgs[patient_imgs['MONTHS'] == current_months].index[0]
        pos = patient_imgs.index.get_loc(idx)
        
        # 앞뒤로 범위를 잡아 3~5장 추출
        start = max(0, pos - (count // 2))
        end = min(len(patient_imgs), start + count)
        
        sequence_df = patient_imgs.iloc[start:end]
        
        return {
            'paths': sequence_df['LOCAL_FMRI_PATH'].tolist(),
            'months': sequence_df['MONTHS'].tolist(),
            'matched_idx': sequence_df['MONTHS'].tolist().index(current_months) # 리스트 중 몇 번째가 당사자인지
        }

    def process_details(self, input_data, input_fmri_path, top_3_records):
        """프론트엔드 상세 페이지용 최종 데이터 패키징"""
        results = []
        
        for res in top_3_records:
            ptid = res['PTID']
            
            # 1. 공통 증상 추출
            common_symptoms = [
                col for col in self.symptom_cols 
                if input_data.get(col) == 1 and res.get(col) == 1
            ]
            
            # 2. 유사도 퍼센트 계산
            sim_percent = max(0, (1 - res['similarity_score']) * 100)
            
            # 3. 상세 리포트 구성
            report = {
                # 기본 정보
                'summary': {
                    'ptid': ptid,
                    'similarity': round(sim_percent, 1),
                    'matched_month': res['MONTHS'],
                    'edu_level': res['EDUCATION_LEVEL'],
                    'mmse': res['ADJUSTED_MMSE']
                },
                # 증상 비교
                'symptoms': {
                    'common': common_symptoms,
                    'input_patient_all': [col for col in self.symptom_cols if input_data.get(col) == 1],
                    'similar_patient_all': [col for col in self.symptom_cols if res.get(col) == 1]
                },
                # MMSE 그래프 데이터
                'mmse_chart': {
                    'similar_patient_history': self.get_patient_history(ptid),
                    'input_patient_score': get_adjusted_mmse(input_data['MMSE_SCORE'], input_data['EDUCATION_LEVEL'])
                },
                # fMRI 시각화 데이터
                'fmri_display': {
                    'sequence': self.get_fmri_sequence(ptid, res['MONTHS']),
                    'input_fmri': input_fmri_path
                }
            }
            results.append(report)
            
        return results