from functools import wraps
from flask import Flask, render_template, request, json, redirect, session, url_for, escape, flash
import mongo as db



app = Flask(
    'FlaskApp',
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
    )



app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = '\xe5\x0fn\xb9\xe7\xdbY\xfa\xcf\xa5\xac\x06\xab\xa7"\xe3\xf6b\xdb\x99U\x9a\xbb\x14'



def requer_login(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session['logged_in']:
            flash('E necessario fazer login!','danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper



@app.route("/", methods=['GET','POST'])
def login():
    user = None
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['password']
        if user == "":
            flash('Nome de usuario invalido!','danger')
        elif passwd == "":
            flash('Senha invalida!','danger')
        else:
            data = db.find_user(user)
            if not data :
                flash('Usuario nao encontrado!','danger')
                return render_template('login.html',user=None)
            elif data['password'] != passwd:
                flash('Senha incorreta!','danger')
                return render_template('login.html',user=user)
            else:
                session['user'] = data['user']
                session['_id'] = str(data['_id'])
                session['logged_in'] = True
                return redirect(url_for('usuarios'))
    return render_template('login.html',user=user)



@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['password']
        valid_passwd = request.form['valid_pass']
        email = request.form['email']
        nascimento = request.form['nascimento']
        data = db.find_user(user)
        if not data:
            if passwd == valid_passwd:
                user_data = {'user':user,'password':passwd,'email':email,'nascimento':nascimento}
                db.insert_user(user_data)
                if not session.get('logged_in'):
                    flash('Usuario cadastrado! Faca login para continuar!','success')
                    return redirect(url_for('login'))
                else:
                    flash('Usuario cadastrado!','success')
                    return redirect(url_for('usuarios'))
            else:
                flash('As senhas nao conferem!','danger')
                return render_template('cadastrar.html',user=data)
        else:
            flash('O usuario ja existe!','danger')
    return render_template('cadastrar.html', user=None)



@app.route('/usuarios')
@requer_login
def usuarios():
    users = db.find_users()
    return render_template('usuarios.html',users=users)



@app.route('/usuarios/apagar/<user>')
@requer_login
def apagar(user):
    db.delete_user(user)
    flash('Usuario apagado!','success')
    return redirect(url_for('usuarios'))



@app.route('/usuarios/editar/<user>', methods=['GET','POST'])
@requer_login
def editar(user):
    if request.method == "POST":
        data = db.find_user(user)
        data['user'] = request.form['user']
        data['nascimento'] = request.form['nascimento']
        db.update_user({'user':user},data)
        flash('Usuario editado!','success')
        return redirect(url_for('usuarios'))
    else:
        data = db.find_user(user)
        return render_template('editar.html',user=data)



@app.route('/logout')
@requer_login
def logout():
    session['logged_in'] = False
    flash('Sessao Logout!','success')
    return redirect(url_for('login'))



app.run(
    host='0.0.0.0',
    extra_files=['templates'],
    use_reloader=True,
    debug=False
    )
