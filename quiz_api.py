from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from models import db, User, Quiz
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/")
def home():
    if 'user' in session:
        return render_template("index.html")
    else:
        return redirect(url_for("quiz.login"))

@quiz_bp.route("/login", methods = ["POST", "GET"])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error = error)
    else:
        if 'username' not in request.form or len(request.form['username']) == 0 or 'password' not in request.form or len(request.form['password']) == 0:
            return render_template('login.html', error = 'Misssing values for login form')
        else:
            username = request.form['username']
            password = request.form['password']
            user_info = User.query.filter_by(username=username).first()
            if not user_info:
                return render_template('login.html', error = 'Invalid login credentials')
            elif user_info.password != password:
                 return render_template('login.html', error = 'Invalid login credentials')
            else:
                session['user'] = username
                session['userid'] = user_info.id
                return redirect(url_for("quiz.home"))

@quiz_bp.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    else:
        if 'username' not in request.form or len(request.form['username']) == 0 or 'password' not in request.form or len(request.form['password']) == 0:
            return render_template('login.html', error = 'Misssing values for register form')
        else:
            username = request.form['username']
            password = request.form['password']
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            user_info = User.query.filter_by(username=username).first()
            session['userid'] = user_info.id
            return redirect(url_for("quiz.home"))
        
@quiz_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("userid", None)
    session.pop("current_question", None)
    session.pop("score", None)
    return redirect(url_for("quiz.login"))

@quiz_bp.route("/quiz", methods = ["GET", "POST"])
def quiz():
    if 'user' not in session:
        return redirect(url_for("quiz.login"))

    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0

    with open('./data/questions.json', 'r') as file:
        questions = json.load(file)

    if request.method == 'GET':
        current_question = session['current_question']
        score = session['score']

        if current_question < len(questions):
            current_quiz_data = questions[current_question]
            return render_template("quiz.html", current_question=current_question+1, current_quiz_data = current_quiz_data)
        else:
            return redirect(url_for("home"))
    
    else:
        current_quiz_data = questions[session['current_question']]
        if 'option' not in request.form or len(request.form['option']) == 0:
            return render_template("quiz.html", current_question=session['current_question']+1, current_quiz_data = current_quiz_data, error = 'Make a selection to continue')
        else:
            option_selected = request.form['option']
            if int(option_selected) == int(current_quiz_data['answer']):
                session['score'] = session['score'] + 1
            session['current_question'] = session['current_question'] + 1
            if session['current_question'] > len(questions) - 1:
                session.pop("current_question", None)
                return redirect(url_for("quiz.results"))
            else:
                if session['current_question'] == len(questions) - 1:
                    return render_template("quiz.html", current_question=session['current_question']+1, current_quiz_data = questions[session['current_question']], isFinalQuestion = True)
                else:
                    return render_template("quiz.html", current_question=session['current_question']+1, current_quiz_data = questions[session['current_question']])
        
@quiz_bp.route('/results')
def results():
    if 'user' not in session:
        return redirect(url_for("quiz.login"))
    else:
        quiz = Quiz(session['userid'], session['score'])
        db.session.add(quiz)
        db.session.commit()
        return render_template("results.html", score=session['score'])

@quiz_bp.route('/reset_quiz')
def reset_quiz():
    session.pop("current_question", None)
    session.pop("score", None)
    return redirect(url_for("quiz.quiz"))

