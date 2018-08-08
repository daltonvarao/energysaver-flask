from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.models.sensors import Sensors
from app.models.data import Data
from app.models.users import Users
from json import loads
from app.controllers.login import login_required
from pprint import pprint
from app.controllers.data import create_data_csv, file

# pagina para a criacao de um sensor
@app.route('/sensors/create', methods=['GET','POST'])
@login_required
def create_sensor():
    if request.method == 'POST':
        sensor = Sensors(
            user=request.form['user'],
            name_sensor = request.form['name_sensor'],
            type_sensor = request.form['type_sensor'],
            model_sensor= request.form['model_sensor'],
            local = request.form['local'],
            device = request.form['device'],
        )
        client_sensor= sensor.to_json()
        client_sensor = loads(client_sensor)
        sensors = Sensors.objects(user=request.form['user'],name_sensor=request.form['name_sensor'])
        if sensors:
            flash('This sensor name already in use!','danger')
            return render_template('sensors/create.html', sensor=client_sensor)
        else:
            sensor.save()
            return redirect(url_for('user',user_id=session.get('id')))
            
    else:
        return render_template('sensors/create.html', sensor=None)


# edita os dados de um sensor
@app.route('/users/user/<user_id>/sensors/sensor/<sensor_id>/edit', methods=['GET','POST'])
@login_required
def edit_sensor(user_id,sensor_id):
    user = Users.objects(id=user_id)
    sensor = Sensors.objects(user=user[0].user, id=sensor_id)
    if request.method == 'POST':       
        sensor.update_one(
            name_sensor = request.form['name_sensor'],
            type_sensor = request.form['type_sensor'],
            model_sensor = request.form['model_sensor'],
            device = request.form['device'],
            local = request.form['local']
        )
        sensors = Sensors.objects.all()
        flash('Success! Sensor updated!','success')
        return redirect(url_for('sensors',sensors=sensors,user_id=user[0].id))
    else:    
        return render_template('sensors/edit.html', sensor=sensor[0])


# apaga um sensor
@app.route('/users/user/<user_id>/sensors/sensor/<sensor_id>/delete')
@login_required
def delete_sensor(user_id,sensor_id):
    user = Users.objects(id=user_id)
    Sensors.objects(user=user[0].user, id=sensor_id).delete()
    sensors = Sensors.objects(user=user[0].user)
    flash('Success! Sensor deleted!','success')
    return redirect(url_for('sensors', sensors=sensors,user_id=user[0].id))
    

# retorna a pagina de dashboard, view dos dados
@app.route('/users/user/<user_id>/sensors/sensor/<sensor_id>/dashboard', methods=['GET','POST'])
@login_required
def dashboard(user_id,sensor_id):
    data = []
    labels = []
    sensor_query = Sensors.objects(user=session.get('user'), id=sensor_id)
    
    # pesquisa de dados por dia
    if request.method == 'POST':
        data = []
        labels = []
        data_day = Data.objects(user=session.get('user'), name_sensor=sensor_query[0]['name_sensor'],day=request.form['day'])
        
        # cria o csv com os dados da pesquisa por dia
        create_data_csv(data_day, file)

        # dados para o plot do grafico na pagina
        for data_q in data_day:
            data.append(data_q.value)
            labels.append(data_q.hour)
        flash('Exibindo %i resultados para %s'%(len(data_day),request.form['day']),'info')
        return render_template('sensors/dashboard.html',sensor=sensor_query[0],data=data,labels=labels)
    
    # quando entra na pagina "dashboard"
    data_query = Data.objects(user=session.get('user'), name_sensor = sensor_query[0]['name_sensor']).limit(750)
    
    # cria o csv para o download
    create_data_csv(data_query, file)
    for data_q in data_query:
        data.append(data_q.value)
        labels.append(data_q.hour)
    
    return render_template('sensors/dashboard.html',sensor=sensor_query[0],data=data,labels=labels)

# retorna uma pagina com todos os sensores de um usuario
@app.route('/users/user/<user_id>/sensors')
@login_required
def sensors(user_id):
    user = Users.objects(id=user_id)
    sensors = Sensors.objects(user=user[0].user)
    return render_template('sensors/sensors.html',sensors=sensors)
