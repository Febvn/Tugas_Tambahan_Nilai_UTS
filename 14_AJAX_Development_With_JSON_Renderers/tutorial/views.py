from pyramid.view import view_config
import json
import datetime

@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return {'project': 'AJAX Development Tutorial'}

@view_config(route_name='api_data', renderer='json')
def api_data(request):
    """Return JSON data for AJAX requests"""
    data = {
        'message': 'Hello from Pyramid API!',
        'timestamp': datetime.datetime.now().isoformat(),
        'items': [
            {'id': 1, 'name': 'Item One', 'value': 100},
            {'id': 2, 'name': 'Item Two', 'value': 200},
            {'id': 3, 'name': 'Item Three', 'value': 300},
        ],
        'status': 'success'
    }
    return data

@view_config(route_name='api_echo', renderer='json', request_method='POST')
def api_echo(request):
    """Echo back JSON data sent in POST request"""
    try:
        # Parse JSON from request body
        if request.content_type == 'application/json':
            data = request.json_body
        else:
            # Handle form data
            data = dict(request.POST)

        # Add server timestamp
        response_data = {
            'echo': data,
            'received_at': datetime.datetime.now().isoformat(),
            'method': request.method,
            'content_type': request.content_type,
            'status': 'echo_success'
        }
        return response_data
    except Exception as e:
        return {
            'error': str(e),
            'status': 'error',
            'received_at': datetime.datetime.now().isoformat()
        }
