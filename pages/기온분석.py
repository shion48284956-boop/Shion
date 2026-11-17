
import streamlit as st
import pandas as pd
from pathlib import Path

# CSV 파일 자동 탐색 및 불러오기
@st.cache_data
def load_data():

    # 현재 파일(pages 폴더)의 상위 폴더
    base_dir = Path(__file__).resolve().parent.parent

    # CSV 파일 찾기
    csv_files = list(base_dir.glob("temperature*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"CSV 파일을 찾을 수 없습니다. 검색 위치: {base_dir}"
        )

    # 파일 이름이 달라도 자동으로 읽기
    required_columns = ["일시", "평균기온(℃)"]
    df = None

    for file_path in csv_files:
        for encoding in ["cp949", "utf-8-sig", "utf-8"]:
            try:
                temp = pd.read_csv(file_path, encoding=encoding)

                if all(col in temp.columns for col in required_columns):
                    df = temp
                    break

            except (UnicodeDecodeError, pd.errors.ParserError):
                continue

        if df is not None:
            break

    if df is None:
        raise ValueError(
            "CSV 파일에서 일시 또는 평균기온(℃) 열을 찾지 못했습니다."
        )

    # 날짜 및 기온 데이터 정리
    df["날짜"] = pd.to_datetime(
        df["일시"],
        format="%b-%y",
        errors="coerce"
    )

    df["평균기온(℃)"] = pd.to_numeric(
        df["평균기온(℃)"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["날짜", "평균기온(℃)"]
    )

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    return df.sort_values("날짜")


df = load_data()
