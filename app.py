from flask import Flask
from quiz_api import quiz_bp
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizappdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret123'
db.init_app(app)

app.register_blueprint(quiz_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)