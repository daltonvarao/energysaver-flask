from app import socketio, app
from app.models.data import Data
from flask_socketio import emit
from app.controllers.login import login_required
from flask import send_file
import datetime
import pandas as pd
import os
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
energy = client["energy"]
data = energy["data"]


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


def create_data_csv(data_query, file):
    df = pd.DataFrame(list(data_query))
    df.to_csv(file)
    

file = path+'data.csv'
@app.route('/<user>/<name_sensor>/download/data.csv')
@login_required
def download_data(user, name_sensor):
    data_query = data.find({"user":user, "name_sensor": name_sensor})
    create_data_csv(data_query, file)
    return send_file('%s'%file)
