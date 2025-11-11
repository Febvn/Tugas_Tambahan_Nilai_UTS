from pyramid.view import view_config, view_defaults
from pyramid.response import Response
import json

# Sample data for demonstration
COMPANIES = {
    'acme': {
        'name': 'Acme Corporation',
        'employees': 150,
        'revenue': 25000000,
        'industry': 'Manufacturing',
        'founded': 1950,
        'headquarters': 'Springfield, IL'
    },
    'globex': {
        'name': 'Globex Corporation',
        'employees': 500,
        'revenue': 75000000,
        'industry': 'Technology',
        'founded': 1985,
        'headquarters': 'New York, NY'
    },
    'initech': {
        'name': 'Initech',
        'employees': 75,
        'revenue': 12000000,
        'industry': 'Software',
        'founded': 1995,
        'headquarters': 'Austin, TX'
    }
}

@view_defaults(route_name='home', renderer='templates/home.html')
class HomeViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def home(self):
        return {
            'title': 'Advanced View Classes Tutorial',
            'companies': list(COMPANIES.keys())
        }

@view_defaults(route_name='hello', renderer='templates/hello.html')
class HelloViews:
    def __init__(self, request):
        self.request = request
        self.name = request.matchdict.get('name', 'World')

    @view_config(request_method='GET')
    def hello(self):
        return {
            'name': self.name,
            'greeting': f'Hello, {self.name}!'
        }

    @view_config(request_method='POST', renderer='json')
    def hello_post(self):
        # Handle POST request to hello endpoint
        data = self.request.json_body if self.request.content_type == 'application/json' else {}
        return {
            'message': f'Hello, {self.name}!',
            'method': 'POST',
            'received_data': data,
            'timestamp': self.request.registry.settings.get('timestamp', 'unknown')
        }

@view_defaults(route_name='company')
class CompanyViews:
    def __init__(self, request):
        self.request = request
        self.company_name = request.matchdict.get('name', '').lower()

    @view_config(request_method='GET', renderer='templates/company.html')
    def company(self):
        if self.company_name not in COMPANIES:
            # Return 404 response
            response = Response('Company not found', status=404)
            return response

        company_data = COMPANIES[self.company_name]
        return {
            'company': company_data,
            'company_key': self.company_name
        }

    @view_config(route_name='company_json', request_method='GET', renderer='json')
    def company_json(self):
        if self.company_name not in COMPANIES:
            return {
                'error': 'Company not found',
                'available_companies': list(COMPANIES.keys())
            }

        company_data = COMPANIES[self.company_name]
        return {
            'company': company_data,
            'company_key': self.company_name,
            'api_version': '1.0'
        }

    @view_config(request_method='PUT', renderer='json')
    def update_company(self):
        if self.company_name not in COMPANIES:
            return {'error': 'Company not found'}

        try:
            update_data = self.request.json_body
            # In a real application, you'd update the database here
            # For demo purposes, we'll just return success
            return {
                'message': f'Company {self.company_name} updated successfully',
                'updated_fields': list(update_data.keys()),
                'company': COMPANIES[self.company_name]
            }
        except Exception as e:
            return {'error': str(e)}

    @view_config(request_method='DELETE', renderer='json')
    def delete_company(self):
        if self.company_name not in COMPANIES:
            return {'error': 'Company not found'}

        # In a real application, you'd delete from database
        # For demo, just return success message
        return {
            'message': f'Company {self.company_name} deleted successfully',
            'deleted_company': COMPANIES[self.company_name]
        }

# Additional view classes demonstrating different patterns

@view_config(route_name='home', request_method='GET', renderer='json', name='api_status')
class APIStatusView:
    def __init__(self, request):
        self.request = request

    def __call__(self):
        return {
            'status': 'API is running',
            'version': '1.0',
            'endpoints': [
                '/ - Home page',
                '/hello/{name} - Greeting page',
                '/company/{name} - Company details',
                '/company/{name}/json - Company JSON API'
            ],
            'companies_available': list(COMPANIES.keys())
        }

# View class with custom predicates
@view_defaults(renderer='templates/debug.html')
class DebugViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', request_method='GET', custom_predicates=[lambda info, request: request.params.get('debug') == 'true'])
    def debug_info(self):
        return {
            'debug_info': {
                'method': self.request.method,
                'url': self.request.url,
                'params': dict(self.request.params),
                'headers': dict(self.request.headers),
                'matchdict': self.request.matchdict
            },
            'companies': COMPANIES
        }
