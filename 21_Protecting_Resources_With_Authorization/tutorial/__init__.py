from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)
from .security import (
    RootFactory,
    groupfinder,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory=RootFactory)

    config.include('pyramid_jinja2')
    config.include('pyramid_tm')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], 
        callback=groupfinder,
        hashalg='sha512',
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('admin', '/admin')
    config.add_route('editor', '/editor')

    config.scan()
    return config.make_wsgi_app()