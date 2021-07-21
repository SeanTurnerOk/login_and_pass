from flask import render_template, session, redirect, request, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)
@app.route('/')
def main():
    return render_template('main.html')
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data={'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash}
        User.save(data)
        return redirect('/')
@app.route('/checker', methods=['POST'])
def checker():
    data={'email':request.form['email']}
    user_in_db=User.getByEmail(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db[0]['password'], request.form['password']):
        flash("Invalid Email/Password")
    session['user_id']=user_in_db[0]['id']
    return redirect('/finish')
@app.route('/finish')
def finish():
    if 'user_id' in session.keys():
        return render_template('finish.html')
    else:
        return redirect('/')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')