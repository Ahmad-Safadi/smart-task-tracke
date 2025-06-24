#task_routes.py

from flask import Blueprint, redirect, session, request, render_template
from app.models import Tasks, Tracker
from app import db

bp = Blueprint('task_routes', __name__)

#========== Toggle ==========#
@bp.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    task = Tasks.query.get_or_404(id)
    tracker = Tracker.query.first()

    try:
        diff = int(task.difficulty)
    except (ValueError, TypeError):
        diff = 1

    if task.State == 'pending':
        task.State = 'done'
        tracker.pending -= 1
        tracker.done += 1
        tracker.difficulty_pending -= diff
        tracker.difficulty_complete += diff
    else:
        task.State = 'pending'
        tracker.done -= 1
        tracker.pending += 1
        tracker.difficulty_complete -= diff
        tracker.difficulty_pending += diff

    session.update({
        'pending': tracker.pending,
        'done': tracker.done,
        'difficulty_complete': tracker.difficulty_complete,
        'difficulty_pending': tracker.difficulty_pending
    })

    db.session.commit()
    return redirect('/home')
#========== End Toggle ==========#


#========== Delete ==========#
@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Tasks.query.get_or_404(id)
    tracker = Tracker.query.first()

    try:
        diff = int(task.difficulty)
    except (ValueError, TypeError):
        diff = 1

    if task.State == 'pending':
        tracker.pending -= 1
        tracker.difficulty_pending -= diff
    else:
        tracker.done -= 1
        tracker.difficulty_complete -= diff

    tracker.deleted_tasks += 1

    session.update({
        'pending': tracker.pending,
        'done': tracker.done,
        'difficulty_complete': tracker.difficulty_complete,
        'difficulty_pending': tracker.difficulty_pending,
        'deleted_tasks': tracker.deleted_tasks
    })

    db.session.delete(task)
    db.session.commit()
    return redirect('/home')
#========== End Delete ==========#


#========== Difficulty ==========#
@bp.route('/difficulty/<int:id>', methods=['POST'])
def difficulty(id):
    task = Tasks.query.get_or_404(id)
    tracker = Tracker.query.first()

    try:
        old = int(task.difficulty)
    except (ValueError, TypeError):
        old = 1

    new = old + 1 if 1 <= old < 5 else 1
    task.difficulty = str(new)

    if task.State == 'pending':
        tracker.difficulty_pending = tracker.difficulty_pending - old + new
        session['difficulty_pending'] = tracker.difficulty_pending
    else:
        tracker.difficulty_complete = tracker.difficulty_complete - old + new
        session['difficulty_complete'] = tracker.difficulty_complete

    db.session.commit()
    return redirect('/home')
#========== End Difficulty ==========#

#========== Delete_All ==========#
@bp.route('/Delete_All', methods=['POST'])
def Delete_All():
    db.session.query(Tracker).delete()
    db.session.query(Tasks).delete()
    db.session.commit()
    
    session.clear()
    
    tracker = Tracker()
    db.session.add(tracker)
    db.session.commit()
    
    session.update({
        'pending': 0,
        'done': 0,
        'difficulty_complete': 0,
        'difficulty_pending': 0,
        'deleted_tasks': 0
    })
    
    return redirect('/home')
#========== End Delete_All ==========#


#========== edit ==========#
@bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task = Tasks.query.get_or_404(id)
    session['id'] = task.id
    return redirect('/edit')
#========== End edit ==========#

