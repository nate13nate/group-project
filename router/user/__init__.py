from flask import request, Blueprint
from flask_cors import cross_origin
from bson.json_util import dumps
from uuid import uuid4
import time

from mongo import db
from service.user import authenticate

user = Blueprint('user', __name__, url_prefix='/user')

@user.post('/login')
@cross_origin()
def login():
    body = request.get_json()

    username, password = [body['username'], body['password']]
    user = db.user.find_one({ 'username': username, 'password': password })

    token = str(uuid4())
    if user is not None:
        db.user.update_one({ '_id': user['_id'] }, { '$set': { 'token': str(token), 'timestamp': round(time.time() * 1000) } })
        return token

    admin = db.admin.find_one({ 'username': username, 'password': password })
    if admin is None:
        raise Exception('User not found')
    
    db.admin.update_one({ '_id': admin['_id'] }, { '$set': { 'token': str(token), 'timestamp': round(time.time() * 1000) } })
    return token

@user.post('/create')
@cross_origin()
def create_user():
    body = request.get_json()
    username, password = [body['username'], body['password']]

    user = db.user.find_one({ 'username': username })
    if user is not None:
        raise Exception('User already exists')

    token = str(uuid4())
    db.user.insert_one({
        'username': username,
        'password': password,
        'token': token,
        'timestamp': round(time.time() * 1000),
    })
    return token

@user.get('/id/<token>')
@cross_origin()
def get_id_from_token(token: str):
    return authenticate(token)[0]

@user.delete('/<token>')
@cross_origin()
def invalidate_token(token: str):
    db.user.update_one({ 'token': token }, { '$set': { 'token': None, 'timestamp': None } })
    db.admin.update_one({ 'token': token }, { '$set': { 'token': None, 'timestamp': None } })
    return token

@user.get('/<token>/admin')
def is_admin(token: str):
    return { 'admin': authenticate(token)[1] }
