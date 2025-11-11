from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='json')
def home(request):
    return {'name': 'Home View'}
