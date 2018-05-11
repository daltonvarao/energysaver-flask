from flask import Flask
from flask_mongoengine import MongoEngine
#from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_mail import Mail

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)

app.secret_key = '\xe5\x0fn\xb9\xe7\xdbY\xfa\xcf\xa5\xac\x06\xab\xa7"\xe3\xf6b\xdb\x99U\x9a\xbb\x14'

app.config.from_object('config')

#mqtt = Mqtt(app)
db = MongoEngine(app)
socketio = SocketIO(app)
mail = Mail(app)

from app.controllers import login, users, sensors, admin, data