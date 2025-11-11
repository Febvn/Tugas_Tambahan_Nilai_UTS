import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from sqlalchemy import engine_from_config

from ..models import (
    DBSession,
    User,
    Base,
)

from ..security import hash_password


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    with transaction.manager:
        # Create admin user
        admin = User(
            name='admin', 
            password=hash_password('admin'), 
            email='admin@example.com',
            role='admin'
        )
        DBSession.add(admin)
        
        # Create editor user
        editor = User(
            name='editor', 
            password=hash_password('editor'), 
            email='editor@example.com',
            role='editor'
        )
        DBSession.add(editor)
        
        # Create viewer user
        viewer = User(
            name='viewer', 
            password=hash_password('viewer'), 
            email='viewer@example.com',
            role='viewer'
        )
        DBSession.add(viewer)