from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
)
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
)

from .models import (
    DBSession,
    User,
)

from .security import (
    check_password,
    hash_password,
)


@view_defaults(renderer='home.html')
class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home', permission='view')
    def home(self):
        user = None
        if self.logged_in:
            user = DBSession.query(User).filter_by(name=self.logged_in).first()
        return {
            'name': 'Home View',
            'user': user,
        }

    @view_config(route_name='login', renderer='login.html')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user = DBSession.query(User).filter_by(name=login).first()
            if user and check_password(password, user.password):
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                  headers=headers)
            message = 'Failed login'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                          headers=headers)

    @view_config(route_name='editor', renderer='editor.html', permission='edit')
    def editor(self):
        user = None
        if self.logged_in:
            user = DBSession.query(User).filter_by(name=self.logged_in).first()
        return {
            'name': 'Editor View',
            'user': user,
        }

    @view_config(route_name='admin', renderer='admin.html', permission='admin')
    def admin(self):
        user = None
        users = DBSession.query(User).all()
        if self.logged_in:
            user = DBSession.query(User).filter_by(name=self.logged_in).first()
        return {
            'name': 'Admin View',
            'user': user,
            'users': users,
        }


@forbidden_view_config(renderer='forbidden.html')
def forbidden_view(request):
    """
    This view is called when a user tries to access a resource they don't have permission for.
    """
    login_url = request.route_url('login', _query={'came_from': request.url})
    if not request.authenticated_userid:
        # User is not logged in, redirect to login
        return HTTPFound(location=login_url)
    
    # User is logged in but doesn't have permission
    return {
        'name': 'Forbidden',
        'message': 'You do not have permission to access this resource.',
        'login_url': login_url,
    }