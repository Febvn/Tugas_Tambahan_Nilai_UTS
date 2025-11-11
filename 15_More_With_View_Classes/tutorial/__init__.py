from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('hello', '/hello/{name}')
    config.add_route('company', '/company/{name}')
    config.add_route('company_json', '/company/{name}/json')
    config.scan('.views')
    return config.make_wsgi_app()
