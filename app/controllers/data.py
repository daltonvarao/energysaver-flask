from app import socketio, app
from app.models.data import Data
from flask_socketio import emit
from app.controllers.login import login_required
from flask import send_file
import datetime
import os

path = os.path.abspath(os.path.dirname(__file__))

def save_data(msg):
    data = Data()
    data.user = msg.get('user')
    data.local = msg.get('local')
    data.device = msg.get('device')
    data.day = msg.get('day')
    data.hour = msg.get('hour')
    data.name_sensor = msg.get('name_sensor')
    data.type_sensor = msg.get('type_sensor')
    data.model_sensor = msg.get('model_sensor')
    data.value = msg.get('value')
    data.save()


def create_data_csv(data_query,file):
    with open(file,'w') as data_file:
        data_file.write('user,local,device,day,hour,name_sensor,type_sensor,model_sensor,value\n')
        for data_q in data_query:
            data_file.write('{user},{local},{device},{day},{hour},{name_sensor},{type_sensor},{model_sensor},{value}\n'.format(
                user=data_q.user,
                local=data_q.local,
                device=data_q.device,
                day=data_q.day,
                hour=data_q.hour,
                name_sensor=data_q.name_sensor,
                type_sensor=data_q.type_sensor,
                model_sensor=data_q.model_sensor,
                value=data_q.value
            ))


file = path+'data.csv'
@app.route('/download/data.csv')
@login_required
def download_data():
    return send_file('%s'%file)
