from flask import request

from main import app

@app.post('/user/create')
def create_user():
    body = request.get_json()

@app.delete('/user/<id>/delete')
def delete_user(id: str):
    body = request.get_json()

@app.post('/user/login')
def login():
    body = request.get_json()
    user, pwd = [body['user'], body['pwd']]

@app.post('/user/<id>/authenticate')
def authenticate(id: str):
    body = request.get_json()

@app.post('/user/<id>/change-username')
def change_username(id: str):
    body = request.get_json()

@app.post('/user/<id>/change-password')
def change_password(id: str):
    body = request.get_json()
