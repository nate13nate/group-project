from flask import request

from main import app

app.post('/group/create')
def create_group():
    body = request.get_json()

app.delete('group/<id>/delete')
def delete_group(id: str):
    body = request.get_json()

app.post('/group/<id>/addowner')
def add_owner(id: str):
    body = request.get_json()

app.post('/group/<id>/removeowner')
def remove_owner(id: str):
    body = request.get_json()

app.post('/group/<id>/addmember')
def add_member(id: str):
    body = request.get_json()

app.post('/group/<id>/removemember')
def remove_member(id: str):
    body = request.get_json()

app.post('/group/<id>/name')
def set_name(id: str):
    body = request.get_json()

app.get('/group/<id>')
def get_group(id: str):
    body = request.get_json()
