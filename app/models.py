from . import db

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TaskName = db.Column(db.String(200), nullable=False)
    State = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(200), nullable=False)

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted_tasks = db.Column(db.Integer, default=0)
    pending = db.Column(db.Integer, default=0)
    done = db.Column(db.Integer, default=0)
    difficulty_complete = db.Column(db.Integer, default=0)
    difficulty_pending = db.Column(db.Integer, default=0)
