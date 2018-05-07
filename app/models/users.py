from app import db

class Users(db.Document):
    name = db.StringField(max_length=50)
    user = db.StringField(max_length=50,unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    birth = db.StringField(required=True)
    is_confirmed = db.BooleanField(default=False)