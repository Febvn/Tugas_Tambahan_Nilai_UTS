from pyramid.view import view_config, view_defaults
from pyramid.response import Response
import json
import time
from datetime import datetime

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
        self.logger = request.logger

    @view_config(request_method='GET')
    def home(self):
        self.logger.info(f"Home page accessed from {self.request.remote_addr}")
        return {
            'title': 'Logging Tutorial',
            'companies': list(COMPANIES.keys())
        }

@view_defaults(route_name='hello', renderer='templates/hello.html')
class HelloViews:
    def __init__(self, request):
        self.request = request
        self.name = request.matchdict.get('name', 'World')
        self.logger = request.logger

    @view_config(request_method='GET')
    def hello(self):
        start_time = time.time()
        self.logger.info(f"Hello page requested for name: {self.name} from {self.request.remote_addr}")

        result = {
            'name': self.name,
            'greeting': f'Hello, {self.name}!'
        }

        end_time = time.time()
        self.logger.debug(f"Hello page rendered in {end_time - start_time:.4f} seconds")

        return result

    @view_config(request_method='POST', renderer='json')
    def hello_post(self):
        self.logger.info(f"POST request to hello endpoint from {self.request.remote_addr}")

        try:
            data = self.request.json_body if self.request.content_type == 'application/json' else {}
            self.logger.debug(f"Received POST data: {data}")

            result = {
                'message': f'Hello, {self.name}!',
                'method': 'POST',
                'received_data': data,
                'timestamp': datetime.now().isoformat(),
                'user_agent': self.request.headers.get('User-Agent', 'Unknown')
            }

            self.logger.info(f"Successfully processed POST request for {self.name}")
            return result

        except Exception as e:
            self.logger.error(f"Error processing POST request: {str(e)}")
            return {'error': 'Invalid request data', 'details': str(e)}

@view_defaults(route_name='company')
class CompanyViews:
    def __init__(self, request):
        self.request = request
        self.company_name = request.matchdict.get('name', '').lower()
        self.logger = request.logger

    @view_config(request_method='GET', renderer='templates/company.html')
    def company(self):
        self.logger.info(f"Company page requested: {self.company_name} from {self.request.remote_addr}")

        if self.company_name not in COMPANIES:
            self.logger.warning(f"Company not found: {self.company_name}")
            response = Response('Company not found', status=404)
            return response

        company_data = COMPANIES[self.company_name]
        self.logger.debug(f"Returning company data for {self.company_name}: {company_data}")

        return {
            'company': company_data,
            'company_key': self.company_name
        }

    @view_config(route_name='company_json', request_method='GET', renderer='json')
    def company_json(self):
        self.logger.info(f"Company JSON API requested: {self.company_name} from {self.request.remote_addr}")

        if self.company_name not in COMPANIES:
            self.logger.warning(f"Company not found in JSON API: {self.company_name}")
            return {
                'error': 'Company not found',
                'available_companies': list(COMPANIES.keys()),
                'timestamp': datetime.now().isoformat()
            }

        company_data = COMPANIES[self.company_name]
        self.logger.debug(f"Returning JSON data for {self.company_name}")

        return {
            'company': company_data,
            'company_key': self.company_name,
            'api_version': '1.0',
            'timestamp': datetime.now().isoformat()
        }

    @view_config(request_method='PUT', renderer='json')
    def update_company(self):
        self.logger.info(f"PUT request to update company: {self.company_name} from {self.request.remote_addr}")

        if self.company_name not in COMPANIES:
            self.logger.warning(f"Attempted to update non-existent company: {self.company_name}")
            return {'error': 'Company not found'}

        try:
            update_data = self.request.json_body
            self.logger.debug(f"Update data received: {update_data}")

            # In a real application, you'd update the database here
            # For demo purposes, we'll just return success
            result = {
                'message': f'Company {self.company_name} updated successfully',
                'updated_fields': list(update_data.keys()),
                'company': COMPANIES[self.company_name],
                'timestamp': datetime.now().isoformat()
            }

            self.logger.info(f"Successfully updated company: {self.company_name}")
            return result

        except Exception as e:
            self.logger.error(f"Error updating company {self.company_name}: {str(e)}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}

    @view_config(request_method='DELETE', renderer='json')
    def delete_company(self):
        self.logger.info(f"DELETE request for company: {self.company_name} from {self.request.remote_addr}")

        if self.company_name not in COMPANIES:
            self.logger.warning(f"Attempted to delete non-existent company: {self.company_name}")
            return {'error': 'Company not found'}

        # In a real application, you'd delete from database
        # For demo, just return success message
        result = {
            'message': f'Company {self.company_name} deleted successfully',
            'deleted_company': COMPANIES[self.company_name],
            'timestamp': datetime.now().isoformat()
        }

        self.logger.info(f"Successfully deleted company: {self.company_name}")
        return result

# Logging demonstration view
@view_config(route_name='logs', renderer='templates/logs.html')
class LogViews:
    def __init__(self, request):
        self.request = request
        self.logger = request.logger

    def __call__(self):
        self.logger.info("Logs page accessed")

        # Demonstrate different log levels
        self.logger.debug("This is a debug message")
        self.logger.info("This is an info message")
        self.logger.warning("This is a warning message")
        self.logger.error("This is an error message")

        # Simulate some processing with timing
        start_time = time.time()
        time.sleep(0.1)  # Simulate processing
        end_time = time.time()

        self.logger.info(f"Log demonstration completed in {end_time - start_time:.4f} seconds")

        return {
            'title': 'Application Logging Demo',
            'log_levels': ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            'current_time': datetime.now().isoformat(),
            'processing_time': f"{end_time - start_time:.4f} seconds"
        }

# Additional view classes demonstrating different patterns

@view_config(route_name='home', request_method='GET', renderer='json', name='api_status')
class APIStatusView:
    def __init__(self, request):
        self.request = request
        self.logger = request.logger

    def __call__(self):
        self.logger.info("API status endpoint accessed")

        return {
            'status': 'API is running',
            'version': '1.0',
            'endpoints': [
                '/ - Home page',
                '/hello/{name} - Greeting page',
                '/company/{name} - Company details',
                '/company/{name}/json - Company JSON API',
                '/logs - Logging demonstration'
            ],
            'companies_available': list(COMPANIES.keys()),
            'timestamp': datetime.now().isoformat(),
            'server_info': {
                'remote_addr': self.request.remote_addr,
                'user_agent': self.request.headers.get('User-Agent', 'Unknown'),
                'method': self.request.method,
                'url': str(self.request.url)
            }
        }

# View class with custom predicates
@view_defaults(renderer='templates/debug.html')
class DebugViews:
    def __init__(self, request):
        self.request = request
        self.logger = request.logger

    @view_config(route_name='home', request_method='GET', custom_predicates=[lambda info, request: request.params.get('debug') == 'true'])
    def debug_info(self):
        self.logger.info("Debug page accessed with debug=true parameter")

        debug_data = {
            'debug_info': {
                'method': self.request.method,
                'url': str(self.request.url),
                'params': dict(self.request.params),
                'headers': dict(self.request.headers),
                'matchdict': self.request.matchdict,
                'remote_addr': self.request.remote_addr,
                'timestamp': datetime.now().isoformat()
            },
            'companies': COMPANIES,
            'log_message': 'This debug information has been logged'
        }

        self.logger.debug(f"Debug data collected: {debug_data['debug_info']}")
        return debug_data
