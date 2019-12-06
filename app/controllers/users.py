from flask import render_template, request, flash, url_for, redirect
from app import app, mail
from flask_mail import Message
from json import loads
from werkzeug.security import generate_password_hash
from app.models.users import Users
from app.models.sensors import Sensors
from app.controllers.login import login_required


@app.route('/users/create', methods=['GET','POST'])
def create_user():
    if request.method == "POST":
        users = Users.objects(user=request.form['user'])
        emails = Users.objects(email=request.form['email'])
        user = Users(
                name=request.form['name'],
                user=request.form['user'],
                email=request.form['email'],
                password=generate_password_hash(request.form['password']),
                birth=request.form['birth']
            )
        # transforma str em json
        client = loads(user.to_json())
        if users:
            flash('This username already in use!','danger')
            return render_template('users/create.html',user=client)
        elif emails:
            flash('This email address already in use!','danger')
            return render_template('users/create.html',user=client)            
        elif request.form['password'] != request.form['confirm_password']:
            flash('Passwords don\'t match!','danger')
            return render_template('users/create.html',user=client)            
        else:
            user.save()
            send_confirmation(user)
            flash('Sucess! Login to continue!','success')
            return redirect(url_for('login'))
    else:
        return render_template('users/create.html',user=None)


@app.route('/users/user/<user_id>')
@login_required
def user(user_id):
    places = [] 
    user_query = Users.objects(id=user_id)
    if user_query:
        client = {
            'name':user_query[0].name,
            'user':user_query[0].user,
            'email':user_query[0].email,
            'birth':user_query[0].birth
            }
        sensors = Sensors.objects(user=client['user'])
        for sensor in sensors:
            places.append(sensor.local)
        
        if not user_query[0].is_confirmed:
            flash('Email not confirmed yet! Check your email address for your security!','danger')

        return render_template('users/user.html',user=client, sensors=sensors,places=set(places))
    else:
        flash('User not found!','danger')
        return redirect(url_for('login'))


def send_confirmation(user):
    subject = "Email confirmation" 
    html = '<h2>Hello, %s</h2><br>'%user.user
    html += '<p>Copy the id below and past to confirmation page to confirm your email.</p><br>'
    html += '<p>Your id: %s'%str(user.id)
    html += '<p>Thank you!</p><nr>'
    html += '<p>Energysaver copyright 2017.</p>'
    msg = Message(
        subject = subject,
        sender ='mydocumentsdy@gmail.com',
        recipients = [str(user.email)],
        html = html)
    mail.send(msg)


@app.route('/users/user/confirm/<user_id>',methods=["GET","POST"])
@login_required
def user_confirm(user_id):
    user = Users.objects(id=user_id)
    if request.method == "POST":
        if request.form['id'] == user_id:
            user.update(is_confirmed=True)
    else:
        if user[0].is_confirmed:
            flash('You has been confirmed your email!','success')
        else:
            flash('Please check your email to confirm!','warning')
            
 
    return render_template('users/confirmation.html',user=user[0])


@app.route('/users/user/<user_id>/local/<local_name>')
@login_required
def places(user_id,local_name):
    user = Users.objects(id=user_id)
    sensors = Sensors.objects(user=user[0].user,local=local_name)
    return render_template('sensors/places.html',sensors=sensors)
