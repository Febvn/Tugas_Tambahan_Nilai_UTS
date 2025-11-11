import logging
from pyramid.config import Configurator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    # Add logging to the configuration
    config.add_request_method(get_logger, 'logger', reify=True)

    config.add_route('home', '/')
    config.add_route('hello', '/hello/{name}')
    config.add_route('company', '/company/{name}')
    config.add_route('logs', '/logs')
    config.scan('.views')
    return config.make_wsgi_app()

def get_logger(request):
    """Add a logger to the request object."""
    return logging.getLogger('tutorial')
