import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["날짜"])
    df["공부시간(시간)"] = df["공부시간(분)"] / 60
    return df

def subject_summary(df):
    return df.groupby("과목")["공부시간(시간)"].sum().sort_values(ascending=False)

def daily_summary(df):
    return df.groupby("날짜")["공부시간(시간)"].sum()

def focus_statistics(df):
    return df.groupby("과목")["집중도"].agg(["mean", "std"]).rename(columns={"mean": "평균집중도", "std": "변동성"})

def generate_feedback(row):
    if row["집중도"] >= 4 and row["공부시간(분)"] >= 90:
        return "몰입도 매우 좋음 👍"
    elif row["집중도"] <= 2:
        return "집중 어려움 😓"
    else:
        return "보통 수준"

def add_feedback(df):
    df["피드백"] = df.apply(generate_feedback, axis=1)
    return df

def create_heatmap_data(df):
    df["요일"] = df["날짜"].dt.day_name()
    return df.pivot_table(index="과목", columns="요일", values="공부시간(시간)", aggfunc="sum").fillna(0)

def generate_summary():
    csv_path = os.path.join(os.path.dirname(__file__), "study_log.csv")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["study_time_hours"] = df["study_time_minutes"] / 60
    subject_summary = df.groupby("subject")["study_time_hours"].sum().sort_values(ascending=False).to_dict()
    focus_stats = df.groupby("subject")["focus_level"].agg(["mean", "std"]).rename(columns={"mean": "평균집중도", "std": "변동성"}).to_dict(orient="index")
    # 최근 5개 피드백
    def feedback(row):
        if row["focus_level"] >= 4 and row["study_time_minutes"] >= 90:
            return "몰입도 매우 좋음 👍"
        elif row["focus_level"] <= 2:
            return "집중 어려움 😓"
        else:
            return "보통 수준"
    df["피드백"] = df.apply(feedback, axis=1)
    recent_feedback = df[["date", "subject", "study_time_minutes", "focus_level", "피드백"]].tail(5).apply(
        lambda row: f"{row['date'].date()} {row['subject']} - {row['피드백']}", axis=1
    ).tolist()
    return subject_summary, focus_stats, recent_feedback

def generate_heatmap_data():
    import os
    csv_path = os.path.join(os.path.dirname(__file__), "study_log.csv")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["study_time_hours"] = df["study_time_minutes"] / 60
    df["요일"] = df["date"].dt.day_name()
    pivot = df.pivot_table(index="subject", columns="요일", values="study_time_hours", aggfunc="sum").fillna(0)
    # Chart.js용 데이터 변환
    heatmap_data = []
    for subject in pivot.index:
        row = {"subject": subject, "values": [pivot.loc[subject, day] for day in pivot.columns]}
        heatmap_data.append(row)
    return heatmap_data