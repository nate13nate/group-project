import time

from mongo import db

TOKEN_LIFETIME = 3600000

def authenticate(token: str):
    if token is None:
        raise Exception('Invalid token')
    user = db.user.find_one({ 'token': token })
    admin = db.admin.find_one({ 'token': token })

    is_admin = admin is not None
    info = admin if is_admin else user
    if info is None:
        raise Exception('Invalid token')
    if 'timestamp' not in info or round(time.time() * 1000) - info['timestamp'] > TOKEN_LIFETIME:
        raise Exception('Invalid token')
    return str(info['_id']), is_admin
