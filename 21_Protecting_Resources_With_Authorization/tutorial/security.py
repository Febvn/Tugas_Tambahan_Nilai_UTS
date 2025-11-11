import bcrypt
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)

from .models import (
    DBSession,
    User,
)


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit'),
        (Allow, 'group:editors', 'edit'),
        (Allow, 'group:admins', 'admin'),
    ]

    def __init__(self, request):
        pass


def groupfinder(userid, request):
    """
    Return the groups (roles) for a given user.
    This callback is used by the authentication policy.
    """
    user = DBSession.query(User).filter_by(name=userid).first()
    if user:
        if user.role == 'admin':
            return ['group:admins', 'group:editors']
        elif user.role == 'editor':
            return ['group:editors']
    return []


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)