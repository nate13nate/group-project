from flask import request

from main import app

app.post('/event/create')
def create_event():
    body = request.get_json()

app.delete('event/<id>/delete')
def delete_event(id: str):
    body = request.get_json()

app.post('/event/<id>/addowner')
def add_owner(id: str):
    body = request.get_json()

app.post('/event/<id>/removeowner')
def remove_owner(id: str):
    body = request.get_json()

app.post('/event/<id>/addparticipant')
def add_participant(id: str):
    body = request.get_json()

app.post('/event/<id>/removeparticipant')
def remove_participant(id: str):
    body = request.get_json()

app.post('/event/<id>/name')
def set_name(id: str):
    body = request.get_json()

app.get('/event/<id>')
def get_event(id: str):
    body = request.get_json()

app.post('/event/<id>/group')
def set_group(id: str):
    body = request.get_json()

app.post('/event/<id>/time')
def set_time(id: str):
    body = request.get_json()

app.post('/event/<id>/location')
def set_location(id: str):
    body = request.get_json()
