from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    """Home page view with session information display."""
    session = request.session

    # Get session data
    username = session.get('username')
    counter = session.get('counter', 0)
    login_time = session.get('login_time')

    return {
        'username': username,
        'counter': counter,
        'login_time': login_time,
        'session_id': session.id if hasattr(session, 'id') else 'N/A',
        'session_keys': list(session.keys()),
    }

@view_config(route_name='login', renderer='templates/login.html', request_method='GET')
def login_form(request):
    """Display login form."""
    return {}

@view_config(route_name='login', renderer='templates/login.html', request_method='POST')
def login_submit(request):
    """Process login form submission."""
    username = request.params.get('username', '').strip()

    if username:
        session = request.session
        session['username'] = username
        session['login_time'] = str(request.datetime)
        session['counter'] = 0

        # Add flash message
        request.session.flash('Welcome, {}! You have been logged in.'.format(username), 'success')

        return HTTPFound(location=request.route_url('home'))
    else:
        request.session.flash('Please enter a username.', 'error')
        return {'error': 'Please enter a username.'}

@view_config(route_name='logout')
def logout(request):
    """Logout user and clear session."""
    session = request.session

    username = session.get('username')
    if username:
        request.session.flash('Goodbye, {}! You have been logged out.'.format(username), 'info')

    # Clear session
    session.invalidate()

    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='counter', renderer='json')
def counter(request):
    """Increment and return counter value."""
    session = request.session

    # Initialize counter if not exists
    if 'counter' not in session:
        session['counter'] = 0

    # Increment counter
    session['counter'] += 1

    return {
        'counter': session['counter'],
        'session_id': session.id if hasattr(session, 'id') else 'N/A'
    }

@view_config(route_name='flash_demo', renderer='templates/flash_demo.html')
def flash_demo(request):
    """Demonstrate flash messages."""
    # Add various types of flash messages
    request.session.flash('This is an informational message.', 'info')
    request.session.flash('This is a success message!', 'success')
    request.session.flash('This is a warning message.', 'warning')
    request.session.flash('This is an error message.', 'error')

    # Get all flash messages
    messages = request.session.pop_flash()

    return {
        'messages': messages,
        'flash_queues': request.session.get_flash_queues()
    }
