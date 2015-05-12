#!/usr/bin/env python
from getpass import getpass
import sys

from flask import current_app
from app import app, bcrypt
from app.models import User, db

def main():
    with app.app_context():
        db.metadata.create_all(db.engine)

        print 'Enter email address: ',
        email = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print 'User added.'


if __name__ == '__main__':
    sys.exit(main())
