from app import db

class Data(db.Document):
    user = db.StringField()
    local = db.StringField()
    device = db.StringField()
    day = db.StringField()
    hour = db.StringField() 
    name_sensor = db.StringField()
    type_sensor = db.StringField()
    model_sensor = db.StringField()
    value = db.FloatField()