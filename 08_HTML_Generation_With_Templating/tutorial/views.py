from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'name': 'Home View'}

@view_config(route_name='hello', renderer='templates/hello.pt')
def hello(request):
    return {'name': 'Hello View'}
