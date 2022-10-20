from flask_app import app
from flask_app import Flask, render_template, request, redirect, session, flash
from flask_app.models import users_models, magazines_models



@app.route('/magazine/create', methods=['POST'])
def create_new_magazine():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    if not magazines_models.Magazine.validate_form(request.form):
        return redirect('/magazine/new')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    magazines_models.Magazine.create_magazine(data)
    return redirect('/dashboard') 

@app.route('/magazine/new')
def magazine_new():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = { 'id': session['id'] }
    return render_template('new_magazine.html', user=users_models.User.get_user_by_id(data)) 

@app.route('/magazine/show/<int:magazine_id>')
def magazine_show_one(magazine_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = { 'id': magazine_id }
    data_user = { 'id': session['id'] }
    return render_template('show_magazine.html', one_magazine=magazines_models.Magazine.get_by_id(data), user=users_models.User.get_user_by_id(data_user))

@app.route('/magazine/edit/<int:magazine_id>')
def edit_magazine(magazine_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = { 'id': magazine_id }
    data_user = { 'id': session['id'] }
    return render_template('edit.html', one_magazine=magazines_models.Magazine.get_by_id(data), user=users_models.User.get_user_by_id(data_user))

@app.route('/magazine/update', methods=['POST'])
def update_magazine():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    if not magazines_models.Magazine.validate_form(request.form):
        id = int(request.form['id'])
        return redirect(f'/magazine/edit/{id}')
    data = {
        'id': int(request.form['id']),
        'title': request.form['title'],
        'description': request.form['description'],
    }
    magazines_models.Magazine.update_magazine(data)
    return redirect('/dashboard') 

@app.route('/magazine/delete/<int:magazine_id>', methods=['POST'])
def delete_magazine(magazine_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = { 'id': magazine_id }
    magazines_models.Magazine.delete_magazine(data)
    return redirect('/dashboard') 

@app.route('/magazine/unsubscribe', methods=['POST'])
def un_subscribe_magazine():
    magazines_models.Magazine.unsubscribe(request.form)
    return redirect('/dashboard')

@app.route('/magazine/subscribe', methods=['POST'])
def subscribe_magazine():
    magazines_models.Magazine.subscribe(request.form)
    return redirect('/dashboard')