from pyramid.httpexceptions import HTTPFound, HTTPGone
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home')
def home(request):
    return Response('Home View')

@view_config(route_name='hello')
def hello(request):
    name = request.matchdict['name']
    return Response(f'Hello {name}!')

@view_config(route_name='redirect')
def redirect(request):
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='gone')
def gone(request):
    return HTTPGone()
