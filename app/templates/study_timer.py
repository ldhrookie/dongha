import gradio as gr
import time
from datetime import datetime

# 내부 상태
session_state = {
    "running": False,
    "start_time": None,
    "logs": [],
    "today_minutes": 0,
    "tier": "Bronze",
    "score": 0,
}

# 점수 및 티어 계산
def update_score_and_tier():
    minutes = session_state["today_minutes"]
    session_state["score"] += minutes
    if minutes > 180:
        session_state["tier"] = "Gold"
    elif minutes > 90:
        session_state["tier"] = "Silver"
    else:
        session_state["tier"] = "Bronze"

# 타이머 시작
def start_timer():
    if not session_state["running"]:
        session_state["start_time"] = datetime.now()
        session_state["running"] = True
    return update_ui()

# 타이머 종료 (자동 점수 반영 포함)
def stop_timer(memo, felt_minutes):
    if session_state["running"]:
        end_time = datetime.now()
        duration = (end_time - session_state["start_time"]).total_seconds() // 60
        log = {
            "start_time": session_state["start_time"],
            "end_time": end_time,
            "duration": int(duration),
            "memo": memo,
            "felt_minutes": int(felt_minutes) if felt_minutes else None
        }
        session_state["logs"].append(log)
        session_state["today_minutes"] += log["duration"]
        session_state["running"] = False
        session_state["start_time"] = None
        update_score_and_tier()  # 여기서 자동 반영!
    return update_ui()

# UI 업데이트
def update_ui():
    elapsed = "00:00"
    if session_state["running"] and session_state["start_time"]:
        diff = datetime.now() - session_state["start_time"]
        minutes, seconds = divmod(int(diff.total_seconds()), 60)
        elapsed = f"{minutes:02d}:{seconds:02d}"
    logs_display = ""
    for log in session_state["logs"]:
        logs_display += f"{log['start_time'].strftime('%H:%M')} ~ {log['end_time'].strftime('%H:%M')} ({log['duration']}분)"
        if log.get("felt_minutes") is not None:
            logs_display += f"\n체감: {log['felt_minutes']}분"
        if log.get("memo"):
            logs_display += f"\n내용: {log['memo']}"
        logs_display += "\n---\n"
    return elapsed, session_state["today_minutes"], logs_display.strip(), session_state["tier"], session_state["score"]

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📚 공부 타이머")

    with gr.Row():
        start_btn = gr.Button("타이머 시작", variant="primary")
        stop_btn = gr.Button("타이머 종료", variant="stop")
    
    elapsed_text = gr.Textbox(label="경과 시간", interactive=False)
    memo_input = gr.Textbox(label="공부 메모")
    felt_input = gr.Number(label="체감 시간(분)", precision=0)

    with gr.Row():
        today_min_box = gr.Textbox(label="오늘 누적 공부 시간", interactive=False)
        tier_box = gr.Textbox(label="내 티어", interactive=False)
        score_box = gr.Textbox(label="내 점수", interactive=False)

    log_display = gr.Textbox(label="오늘의 공부 기록", lines=10, interactive=False)

    # 이벤트 연결
    start_btn.click(start_timer, outputs=[elapsed_text, today_min_box, log_display, tier_box, score_box])
    stop_btn.click(stop_timer, inputs=[memo_input, felt_input], outputs=[elapsed_text, today_min_box, log_display, tier_box, score_box])

demo.launch()
