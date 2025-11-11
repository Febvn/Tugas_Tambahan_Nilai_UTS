from pyramid.view import view_config, view_defaults

@view_defaults(route_name='home', renderer='string')
class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def home(self):
        return 'Home View'

    @view_config(request_method='POST')
    def home_post(self):
        return 'Home View POST'

@view_defaults(route_name='hello', renderer='string')
class HelloViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def hello(self):
        return 'Hello View'

    @view_config(request_method='POST')
    def hello_post(self):
        return 'Hello View POST'
