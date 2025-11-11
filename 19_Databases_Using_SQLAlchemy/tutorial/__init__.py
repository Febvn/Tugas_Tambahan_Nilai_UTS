from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import os
import sys

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)
