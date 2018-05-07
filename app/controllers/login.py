from flask import render_template, request, redirect, flash, session, url_for
from app import app
from app.models.users import Users
from werkzeug.security import check_password_hash
from json import loads
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('logged_in'):
            flash('Login required!','danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/login')
@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        client = request.form['user']
        client_password = request.form['password']
        # busca usuario no banco de dados
        user=Users.objects(user=client)
        if user:
            if check_password_hash(user[0].password,client_password):
                session['logged_in'] = True
                session['user'] = user[0]['user']
                session['name'] = user[0]['name']
                session['id'] = str(user[0]['id'])
                return redirect('/users/user/'+session.get('id'))
            else:
                flash('Wrong password, try again!','danger')
                return render_template('login/index.html',user=client)
        else:
            flash('User not found, try another username!','danger')
    return render_template('login/index.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')