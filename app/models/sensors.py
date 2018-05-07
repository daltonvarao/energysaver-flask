from app import db

class Sensors(db.Document):
    user = db.StringField(required=True)
    name_sensor = db.StringField(required=True)
    model_sensor = db.StringField(required=True)
    type_sensor = db.StringField(required=True)
    local = db.StringField(required=True)
    device = db.StringField(required=True)
