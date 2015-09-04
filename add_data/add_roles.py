#!/usr/bin/env python
import sys
from app import create_app
from app.models import Role


def main(app=create_app()):
    with app.app_context():
        Role.insert_roles()

    print 'Added roles'


if __name__ == '__main__':
    sys.exit(main())
