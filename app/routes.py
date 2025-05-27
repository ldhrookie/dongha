from flask import Blueprint, render_template
from .analysis import generate_summary, generate_heatmap_data
import pandas as pd
import os

def get_daily_trend():
    csv_path = os.path.join(os.path.dirname(__file__), "study_log.csv")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["study_time_hours"] = df["study_time_minutes"] / 60
    trend = df.groupby("date")["study_time_hours"].sum().sort_index()
    return trend

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    subject_summary, focus_stats, recent_feedback = generate_summary()
    daily_trend = get_daily_trend().to_dict()
    heatmap_data = generate_heatmap_data()
    heatmap_days = []
    if heatmap_data and len(heatmap_data) > 0:
        heatmap_days = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        # 실제 데이터에 있는 요일 순서로 맞추고 싶으면 아래처럼
        # heatmap_days = [day for day in df['요일'].unique()]
    return render_template(
        'index.html',
        subject_summary=subject_summary,
        focus_stats=focus_stats,
        recent_feedback=recent_feedback,
        daily_trend=daily_trend,
        heatmap_data=heatmap_data,
        heatmap_days=heatmap_days
    )

@bp.route('/summary')
def summary():
    subject_summary, focus_stats, recent_feedback = generate_summary()
    return render_template('summary.html', subject_summary=subject_summary, focus_stats=focus_stats, recent_feedback=recent_feedback)

@bp.route('/heatmap')
def heatmap():
    heatmap_data = generate_heatmap_data()
    return render_template('heatmap.html', heatmap_data=heatmap_data)