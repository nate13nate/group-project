from flask import request, Blueprint
from bson.json_util import dumps
from bson.objectid import ObjectId

from mongo import db
from service.user import authenticate

group = Blueprint('group', __name__, url_prefix='/group')

@group.get('/user/<token>')
def get_groups_of_user(token: str):
    id, admin = authenticate(token)
    groups = db.group.find({ '$or': [{ 'owners': id }, { 'members': id }] }) if not admin else db.group.find({})
    return dumps(list(groups))

@group.get('/<id>')
def get_group(id: str):
    token = request.args.get('token')
    getEvents = request.args.get('getEvents')
    userId, admin = authenticate(token)

    group = db.group.find_one({ '_id': ObjectId(id) })
    if group is None: raise Exception('No group found')
    if not admin and userId not in group['owners'] and userId not in group['members']: raise Exception('User requesting group is not a part of the group')

    if getEvents == 'true':
        events = db.event.find({ 'group': id })
        group['events'] = events

    return dumps(group)

@group.put('/')
def upsert_group():
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)
    update = body['group']

    if 'id' in body:
        db.group.update_one({ '_id': ObjectId(body['id']) }, { '$set': update })
        return body['id']
    
    owners = update['owners'] if 'owners' in update else []
    if userId not in owners: owners.append(userId)
    update['owners'] = owners
    
    res = db.group.insert_one(update)
    return str(res.inserted_id)

@group.delete('/<id>')
def delete_group(id: str):
    body = request.get_json(force=True)
    token = body['token']
    userId, admin = authenticate(token)

    db.group.delete_one({ '_id': ObjectId(id), 'owners': userId }) if not admin else db.group.delete_one({ '_id': ObjectId(id) })

    return id

@group.post('/<id>/member')
def add_member(id: str):
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)
    if admin: return 'Admins cannot join groups'
    if 'userId' in body: userId = body['userId']

    group = db.group.find_one({ '_id': ObjectId(id) })

    members = group['members']
    if userId in members or userId in group['owners']: return 'Already in group'
    members.append(userId)
    db.group.update_one({ '_id': ObjectId(id) }, { '$set': { 'members': members } })

    return 'Success'

@group.get('/<id>/members')
def get_group_members(id: str):
    token = request.args.get('token')
    authenticate(token)

    group = db.group.find_one({ '_id': ObjectId(id) })

    members = group['members'] if 'members' in group else []
    owners = group['owners'] if 'owners' in group else []

    memberNum = len(members)

    for owner in owners:
        members.append(owner)
    
    output = []
    i = 0
    for memberId in members:
        member = db.user.find_one({ '_id': ObjectId(memberId) })
        if member is None: continue
        output.append({ 'id': memberId, 'username': member['username'], 'owner': i >= memberNum })
        i += 1
    
    return output

@group.delete('/<id>/member/<memberId>')
def remove_member(id: str, memberId: str):
    body = request.get_json()
    token = body['token']
    userId, admin = authenticate(token)

    query = {'_id': ObjectId(id) } if admin or userId == memberId else { '_id': ObjectId(id), 'owners': userId }

    group = db.group.find_one(query)
    if group is None: raise Exception('Group not found')

    members = group['members'] if 'members' in group else []
    if memberId in members: members.remove(memberId)

    db.group.update_one({ '_id': ObjectId(id) }, { '$set': { 'members': members } })
    return id
