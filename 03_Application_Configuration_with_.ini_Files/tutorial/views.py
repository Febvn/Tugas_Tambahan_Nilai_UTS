from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='string')
def home(request):
    return 'Welcome!'


@view_config(route_name='hello', renderer='string')
def hello(request):
    return 'Hello!'
