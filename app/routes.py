<<<<<<< HEAD
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
=======
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, User, StudyLog
from datetime import datetime, timedelta
import pytz

Cutline_point=[0,100,300,500,700,1000,1300,1600,2000,2400,2800,3400,4000,4600,5400,6200,7000,8000,9000,10000,1000000000]
Daily_required=[0,0,10,20,30,40,50,60,80,100,120,140,160,180,210,240,270,300,330,360]
Maximum=[80,100,100,100,100,100,100,100,100,100,120,120,120,120,120,120,150,150,150,150]
Minimum=[0,-25,-25,-25,-50,-50,-50,-75,-75,-75,-100,-100,-100,-150,-150,-150,-200,-200,-200,-300]
Avoid_fall=[True,True,True,True,True,True,True,True,True,True,True,False,False,True,False,False,False,False,False,False]
Tier=['루키','브론즈1','브론즈2','브론즈3','실버1','실버2','실버3','골드1','골드2','골드3','다이아1','다이아2','다이아3','크리스탈1','크리스탈2','크리스탈3','레전드1','레전드2','레전드3','얼티밋']

def update_tier_and_score(rank, rank_point, study_time):
    change = max(Minimum[rank], min(Maximum[rank], (study_time - Daily_required[rank])))
    msg = ""
    if rank_point + change >= Cutline_point[rank+1]:
        rank_point += change
        rank += 1
        msg = f"티어가 상승했습니다: {Tier[rank-1]} -> {Tier[rank]}\n점수가 상승했습니다: {rank_point-change} -> {rank_point} ({change})"
    elif rank_point + change < Cutline_point[rank]:
        if Avoid_fall[rank]:
            change = rank_point - Cutline_point[rank]
            rank_point = Cutline_point[rank]
            msg = f"티어 강등이 방지되었습니다: {Tier[rank]}\n점수가 하락했습니다: {rank_point-change} -> {rank_point} ({change})"
        else:
            rank_point += change
            rank -= 1
            msg = f"티어가 강등되었습니다: {Tier[rank+1]} -> {Tier[rank]}\n점수가 하락했습니다: {rank_point-change} -> {rank_point} ({change})"
    else:
        rank_point += change
        msg = f"점수가 변동되었습니다: {rank_point-change} -> {rank_point} ({change})"
    return rank, rank_point, Tier[rank], msg
>>>>>>> 3d83fe7 (모든 변경사항 푸쉬4)

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

@bp.route('/study', methods=['GET', 'POST'])
@login_required
def study():
    seoul = pytz.timezone('Asia/Seoul')
    now = datetime.now(seoul)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_logs = StudyLog.query.filter(
        StudyLog.user_id == current_user.id,
        StudyLog.start_time >= today_start,
        StudyLog.end_time != None
    ).order_by(StudyLog.start_time.desc()).all()
    today_minutes = sum(
        int((log.end_time - log.start_time).total_seconds() // 60)
        for log in today_logs
    )
    running_log = StudyLog.query.filter_by(user_id=current_user.id, end_time=None).first()
    msg = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start':
            if running_log:
                flash('이미 타이머가 실행 중입니다.')
            else:
                log = StudyLog(user_id=current_user.id, start_time=datetime.now(seoul))
                db.session.add(log)
                db.session.commit()
                flash('타이머 시작!')
        elif action == 'stop':
            if not running_log:
                flash('실행 중인 타이머가 없습니다.')
            else:
                running_log.end_time = datetime.now(seoul)
                memo = request.form.get('memo', '').strip()
                felt_minutes = request.form.get('felt_minutes')
                try:
                    felt_minutes = int(felt_minutes)
                except (TypeError, ValueError):
                    felt_minutes = None
                running_log.memo = memo
                running_log.felt_minutes = felt_minutes
                db.session.commit()
                flash('타이머 종료! 공부기록이 저장되었습니다.')
        elif action == 'apply':
            rank = Tier.index(current_user.tier)
            rank_point = current_user.score
            new_rank, new_score, new_tier, msg = update_tier_and_score(rank, rank_point, today_minutes)
            current_user.score = new_score
            current_user.tier = new_tier
            db.session.commit()
            flash(f"오늘 공부시간: {today_minutes}분\n" + msg)
        return redirect(url_for('main.study'))
    return render_template('study_timer.html',
                           today_minutes=today_minutes,
                           running_log=running_log,
                           today_logs=today_logs)
@bp.route('/heatmap')
@login_required
def heatmap():
    seoul = pytz.timezone('Asia/Seoul')
    now = datetime.now(seoul)
    # 최근 7일간의 날짜
    days = [(now - timedelta(days=i)).date() for i in range(6, -1, -1)]
    # 각 날짜별 공부시간(분) 합계
    heatmap_data = []
    for day in days:
        day_start = seoul.localize(datetime.combine(day, datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        logs = StudyLog.query.filter(
            StudyLog.user_id == current_user.id,
            StudyLog.start_time >= day_start,
            StudyLog.start_time < day_end,
            StudyLog.end_time != None
        ).all()
        total_minutes = sum(
            int((log.end_time - log.start_time).total_seconds() // 60)
            for log in logs
        )
        heatmap_data.append({
            "date": day.strftime('%Y-%m-%d'),
            "minutes": total_minutes
        })
    return render_template('heatmap.html', heatmap_data=heatmap_data)