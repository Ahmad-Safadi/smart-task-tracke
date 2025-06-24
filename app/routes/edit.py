#edit.py

from flask import Blueprint, render_template, request, redirect, url_for,session
from app import db
from app.models import Tasks

bp = Blueprint('edit', __name__)

@bp.route('/edit', methods=['GET', 'POST'])
def edit():
    task_id = session.get('id')
    if not task_id:
        return redirect('/home')

    task = Tasks.query.get_or_404(task_id)

    if request.method == 'POST':
        new_name = request.form.get('Task')
        if new_name:
            task.TaskName = new_name
            db.session.commit()
            return redirect('/home')

    return render_template('edit.html', name=task.TaskName)