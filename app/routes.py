from flask import Blueprint, render_template
from .analysis import generate_summary, generate_heatmap_data

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/summary')
def summary():
    subject_summary, focus_stats, recent_feedback = generate_summary()
    return render_template('summary.html', subject_summary=subject_summary, focus_stats=focus_stats, recent_feedback=recent_feedback)

@bp.route('/heatmap')
def heatmap():
    heatmap_data = generate_heatmap_data()
    return render_template('heatmap.html', heatmap_data=heatmap_data)