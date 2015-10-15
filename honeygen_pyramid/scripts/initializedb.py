import os
import sys

from sqlalchemy import engine_from_config
from pyramid_sqlalchemy import Session
import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars

from honeygen_pyramid.base_model import BaseModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    from honeygen_pyramid.src import User, Address
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    BaseModel.metadata.create_all(engine)
    with transaction.manager:
        brendan = User(name='Brendan', age=18)
        Session.add(brendan)
        Session.flush()

        brendan_address = Address(city='Paris', owner_id=brendan.id)
        Session.add(brendan_address)
        Session.flush()

        john = User(name='John', age=19, best_friend_id=brendan.id)
        Session.add(john)
        Session.flush()

        antoine = User(name='Antoine', age=20)
        Session.add(antoine)
        Session.flush()
