import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# CSV 파일 불러오기
df = pd.read_csv("study_log.csv", parse_dates=["날짜"])

# 기본 전처리
df["공부시간(시간)"] = df["공부시간(분)"] / 60

# 📊 1. 과목별 총 공부 시간
subject_summary = df.groupby("과목")["공부시간(시간)"].sum().sort_values(ascending=False)
print("과목별 총 공부 시간:\n", subject_summary, "\n")

# 📈 2. 날짜별 공부 시간 트렌드
daily_summary = df.groupby("날짜")["공부시간(시간)"].sum()

plt.figure(figsize=(10, 4))
daily_summary.plot(kind="line", marker="o")
plt.title("날짜별 총 공부 시간")
plt.xlabel("날짜")
plt.ylabel("공부시간 (시간)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🧠 3. 집중도 분석
focus_stats = df.groupby("과목")["집중도"].agg(["mean", "std"]).rename(columns={"mean": "평균집중도", "std": "변동성"})
print("과목별 집중도 통계:\n", focus_stats, "\n")

# 🔥 4. 피드백 생성 (간단)
def generate_feedback(row):
    if row["집중도"] >= 4 and row["공부시간(분)"] >= 90:
        return "몰입도 매우 좋음 👍"
    elif row["집중도"] <= 2:
        return "집중 어려움 😓"
    else:
        return "보통 수준"

df["피드백"] = df.apply(generate_feedback, axis=1)
print("최근 피드백 미리보기:\n", df[["날짜", "과목", "공부시간(분)", "집중도", "피드백"]].tail(5), "\n")

# (선택) 📚 5. 히트맵: 과목 vs 요일
df["요일"] = df["날짜"].dt.day_name()
pivot = df.pivot_table(index="과목", columns="요일", values="공부시간(시간)", aggfunc="sum").fillna(0)

plt.figure(figsize=(8, 5))
sns.heatmap(pivot, annot=True, cmap="YlGnBu")
plt.title("요일별 과목별 공부량 히트맵")
plt.tight_layout()
plt.show()
