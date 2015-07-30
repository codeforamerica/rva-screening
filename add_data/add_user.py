#!/usr/bin/env python
from getpass import getpass
import sys

from flask import current_app
from app import create_app, bcrypt
from app.models import AppUser, db

def main():
  app = create_app()
  with app.app_context():
    db.metadata.create_all(db.engine)

    print 'Enter email address: ',
    email = raw_input()
    password = getpass()
    assert password == getpass('Password (again):')

    user = AppUser(
      email=email,
      password=bcrypt.generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    print 'User added.'

if __name__ == '__main__':
    sys.exit(main())
