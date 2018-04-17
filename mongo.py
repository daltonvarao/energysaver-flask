from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client['flask']
users = db['users'] 

# usuario
def insert_user(user):
    try:
        users.insert_one(user)
    except:
        pass

def find_user(user):
    try:
        return users.find_one({'user':user})
    except:
        pass

def update_user(old,new):
    try:
        users.update_one(old,{'$set':new})
    except:
        pass

def delete_user(user):
    try:
        users.delete_one({'user':user})
    except:
        pass

# usuarios
def find_users():
    try:
        return users.find()
    except:
        pass