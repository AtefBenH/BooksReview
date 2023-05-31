from flask_app import app
from flask import render_template, redirect, request, session, jsonify
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/users/create', methods = ['POST'])
def create_user():
    errors = User.validate(request.form)
    if len(errors)==0:
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        data = {
                **request.form, 'password':hashed_password
            }
        session['user_id'] = User.save(data)
        return jsonify({'errors' : []})
    return jsonify({'errors' : errors})

@app.route('/login', methods = ['POST'])
def login():
    user_from_db = User.get_by_email({'email' : request.form['email']})
    if user_from_db :
        if bcrypt.check_password_hash(user_from_db.password, request.form['password']):
            session['user_id'] = user_from_db.id
            return jsonify({'message' : "success"})
    return jsonify({'message' : "Error"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')