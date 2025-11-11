from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Configure session factory
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')

    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('counter', '/counter')
    config.add_route('flash_demo', '/flash')
    config.scan('.views')
    return config.make_wsgi_app()
