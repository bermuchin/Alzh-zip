import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'ADSXLIST_final_with_paths.csv')

def get_adjusted_mmse(raw_score, edu_level):
    if edu_level == 0:
        return min(30, raw_score + 1)
    return raw_score

def load_and_preprocess():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    
    # 1. 날짜 데이터 미리 변환 및 기준일 설정
    df['VISDATE'] = pd.to_datetime(df['VISDATE'], errors='coerce')
    baseline_dates = df.groupby('PTID')['VISDATE'].transform('min')

    # 2. 하이브리드 VISCODE 처리 함수
    def parse_viscode_custom(row):
        code = str(row['VISCODE']).lower().strip()
        
        # (1) 기본 로직: bl은 0, mXX는 숫자 추출
        if code == 'bl':
            return 0
        elif code.startswith('m'):
            try:
                return int(code.replace('m', ''))
            except ValueError:
                pass # m 뒤에 숫자가 없는 경우 등은 아래 날짜 로직으로 이동
        
        # (2) 예외 로직: uns1 등은 날짜 차이로 계산
        if pd.notna(row['VISDATE']) and pd.notna(baseline_dates[row.name]):
            diff_days = (row['VISDATE'] - baseline_dates[row.name]).days
            return int(round(diff_days / 30.0))
        
        return 0 # 정 안되면 0

    # 함수 적용 (행 단위 처리를 위해 axis=1 사용)
    df['MONTHS'] = df.apply(parse_viscode_custom, axis=1)

    # 3. 학력 보정 및 증상 수치화
    df['ADJUSTED_MMSE'] = df.apply(
        lambda x: get_adjusted_mmse(x['MMSE_SCORE'], x['EDUCATION_LEVEL']), axis=1
    )

    symptom_cols = [col for col in df.columns if col.startswith('AX')]
    for col in symptom_cols:
        df[col] = df[col].fillna(1).apply(lambda x: 1 if x == 2 else 0)

    # 4. 시계열 변화량 계산
    df = df.sort_values(['PTID', 'MONTHS'])
    df['MMSE_CHANGE'] = df.groupby('PTID')['ADJUSTED_MMSE'].diff().fillna(0)

    return df