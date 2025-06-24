#home_routes.py

from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models import Tasks, Tracker
from app import db
from sqlalchemy import func

bp = Blueprint('home_routes', __name__)

@bp.route('/home', methods=['POST', 'GET'])
def home():
    max_id = db.session.query(func.max(Tasks.id)).scalar()
    session['id'] = max_id

    tasks = Tasks.query.all()
    tracker = Tracker.query.first()

    if not tracker:
        tracker = Tracker()
        db.session.add(tracker)
        db.session.commit()

    tracker.pending = 0
    tracker.done = 0
    tracker.difficulty_complete = 0
    tracker.difficulty_pending = 0

    for task in tasks:
        try:
            diff = int(task.difficulty)
        except (ValueError, TypeError):
            diff = 1

        if task.State == 'pending':
            tracker.pending += 1
            tracker.difficulty_pending += diff
        else:
            tracker.done += 1
            tracker.difficulty_complete += diff

    session.update({
        'pending': tracker.pending,
        'done': tracker.done,
        'difficulty_complete': tracker.difficulty_complete,
        'difficulty_pending': tracker.difficulty_pending
    })

    db.session.commit()

    if request.method == 'POST':
        task_name = request.form.get('Task')
        difficulty = request.form.get('difficulty')
        send = request.form.get('Send')
        Edit = request.form.get('Edit')
        
        if send and task_name:
            new_task = Tasks(TaskName=task_name, difficulty=difficulty, State='pending')
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home')
                    
    return render_template('home.html', tasks=tasks)