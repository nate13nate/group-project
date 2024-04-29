from flask import request, Blueprint
from bson.json_util import dumps
from bson.objectid import ObjectId

from service.user import authenticate
from mongo import db

event = Blueprint('event', __name__, url_prefix='/event')

@event.get('/user/<token>')
def get_events_of_user(token: str):
    id, admin = authenticate(token)
    events = db.event.find({ '$or': [{ 'owners': id }, { 'members': id }] }) if not admin else db.event.find()
    return dumps(list(events))

@event.get('/<id>')
def get_event(id: str):
    token = request.args.get('token')
    userId, admin = authenticate(token)

    event = db.event.find_one({ '_id': ObjectId(id) })
    if event is None: raise Exception('No event found')

    if admin or userId in event['owners'] or userId in event['members']: return dumps(event)
    raise Exception('User requesting event is not a part of the event')

@event.post('/<id>/member')
def add_member(id: str):
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)
    if admin: return 'Admins cannot join events'

    if 'userId' in body: userId = body['userId']

    event = db.event.find_one({ '_id': ObjectId(id) })

    members = event['members']
    if userId in members or userId in event['owners']: return 'Already in event'
    members.append(userId)
    db.event.update_one({ '_id': ObjectId(id) }, { '$set': { 'members': members } })

    return 'Success'

@event.put('/')
def upsert_event():
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)
    update = body['event']

    if 'id' in body:
        db.event.update_one({ '_id': ObjectId(body['id']) }, { '$set': update })
        return body['id']
    
    owners = update['owners'] if 'owners' in update else []
    if userId not in owners: owners.append(userId)
    update['owners'] = owners
    
    res = db.event.insert_one(update)
    return str(res.inserted_id)

@event.delete('/<id>')
def delete_event(id: str):
    body = request.get_json(force=True)
    token = body['token']
    userId, admin = authenticate(token)

    db.event.delete_one({ '_id': ObjectId(id), 'owners': userId }) if not admin else db.event.delete_one({ '_id': ObjectId(id) })

    return id

@event.get('/<id>/members')
def get_event_members(id: str):
    token = request.args.get('token')
    authenticate(token)

    event = db.event.find_one({ '_id': ObjectId(id) })

    members = event['members'] if 'members' in event else []
    owners = event['owners'] if 'owners' in event else []

    memberNum = len(members)

    for owner in owners:
        members.append(owner)
    
    output = []
    i = -1
    for memberId in members:
        i += 1
        member = db.user.find_one({ '_id': ObjectId(memberId) })
        if member is None:
            continue
        output.append({ 'id': memberId, 'username': member['username'], 'owner': i >= memberNum  })
    
    return output

@event.delete('/<id>/member/<memberId>')
def remove_member(id: str, memberId: str):
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)

    query = {'_id': ObjectId(id) } if userId == memberId or admin else { '_id': ObjectId(id), 'owners': userId }

    event = db.event.find_one(query)
    if event is None: raise Exception('Event not found')

    members = event['members'] if 'members' in event else []
    if memberId in members: members.remove(memberId)

    db.event.update_one({ '_id': ObjectId(id) }, { '$set': { 'members': members } })
    return id
