import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("Iris.csv", encoding="cp949")

# 데이터 기본 정보
print(df.head())
print(df.info())
print(df.describe())

# 품종별 데이터 개수
print(df["품종"].value_counts())

# 품종별 평균 비교
print(df.groupby("품종").mean(numeric_only=True))

# 결측치 확인
print(df.isnull().sum())

# 중복 데이터 확인
print(df.duplicated().sum())

# 상관관계 분석
print(df.corr(numeric_only=True))
