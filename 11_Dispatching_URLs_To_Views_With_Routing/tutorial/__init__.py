from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('hello', '/howdy/{name}')
    config.add_route('redirect', '/goto')
    config.add_route('gone', '/gone')
    config.scan('.views')
    return config.make_wsgi_app()
