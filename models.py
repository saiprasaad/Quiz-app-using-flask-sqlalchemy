from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    def __init__(self, user_id, score):
        self.user_id = user_id
        self.score = score

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    def __init__(self, username, password):
        self.username = username
        self.password = password