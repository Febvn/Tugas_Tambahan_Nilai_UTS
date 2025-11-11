from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static/')

    config.add_route('home', '/')
    config.add_route('contact', '/contact')
    config.add_route('user_form', '/user')
    config.add_route('sequence_form', '/sequence')
    config.scan('.views')
    return config.make_wsgi_app()
