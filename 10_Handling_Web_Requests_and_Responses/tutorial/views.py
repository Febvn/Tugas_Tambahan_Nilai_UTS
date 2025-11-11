from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home', request_method='GET')
def home(request):
    return Response('Home View')

@view_config(route_name='hello', request_method='GET')
def hello(request):
    return Response('Hello View')

@view_config(route_name='home', request_method='POST')
def home_post(request):
    return Response('Home View POST')

@view_config(route_name='hello', request_method='POST')
def hello_post(request):
    return Response('Hello View POST')
