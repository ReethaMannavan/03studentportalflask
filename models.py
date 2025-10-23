from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
