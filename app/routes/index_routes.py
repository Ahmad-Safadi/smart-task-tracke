#index_routes.py

from flask import Blueprint, render_template, request, redirect, session
from app.models import Tracker
from app import db

bp = Blueprint('index_routes', __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        home = request.form['Home']
        if home:
            session['pending'] = 0
            session['done'] = 0
            session['difficulty_complete'] = 0
            session['difficulty_pending'] = 0
            session['deleted_tasks'] = 0
            tracker = Tracker.query.first()
            if not tracker:
                tracker = Tracker()
                db.session.add(tracker)
                db.session.commit()
            return redirect('/home')
    return render_template('index.html')