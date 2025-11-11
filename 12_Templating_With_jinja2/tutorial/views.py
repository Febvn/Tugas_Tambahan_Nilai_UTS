from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return {'name': 'Home View'}

@view_config(route_name='hello', renderer='templates/hello.html')
def hello(request):
    name = request.matchdict['name']
    return {'name': name}
