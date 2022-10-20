from itertools import count
from flask_app import app
from flask_app.models.magazines_models import Magazine
from flask_app.models.users_models import User
from flask import render_template, request, redirect, session, url_for
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, Bcrypt

 
@app.route('/')
def index():
    return render_template('login_register.html')

@app.route('/register', methods=['POST'])
def regitster():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': Bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.create_user(data)
    if user_id:
        session['id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = {'id': session['id']}
    one_user = User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
    #all_magazines = Magazine.()
    return render_template('dashboard.html', one_user=one_user,data_magazines = Magazine.get_all())

@app.route('/user/account')
def display_user_acct():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = {
        'id': session['id']
    }
    one_user = User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
   
    return render_template('account.html', one_user=one_user, all_magazines=Magazine.get_all())


@app.route('/user/account/update', methods=['POST'])
def user_update():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    if not User.validate_account(request.form):
        return redirect(f'/user/account')

    data = {
        'id': session['id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    User.update_user(data)
    flash("Success! Your info has changed", "success")
    return redirect('/user/account')

@app.route('/login', methods=['POST'])
def login():
    data = { 'email': request.form['email'] }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email or Need to register", "danger")
        return redirect('/')
    if not Bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("The password must match and be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
        return redirect('/')
    session['id'] = user_in_db.id
    flash("Login valido")
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')