from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    db_task_title = db.Column(db.String(100), nullable = False)
    deadline = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default = "Pending" )
    deadline_status = db.Column(db.String(100), default='Yet to Finish', nullable=True)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable = False)