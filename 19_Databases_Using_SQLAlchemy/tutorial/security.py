from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Allow,
    Everyone,
)


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:editors', 'edit'),
    ]

    def __init__(self, request):
        pass
