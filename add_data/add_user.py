#!/usr/bin/env python
from getpass import getpass
import sys
from flask.ext.security.utils import encrypt_password

from app import create_app
from app.models import AppUser, db, Service, Role


def main():
    app = create_app()
    with app.app_context():
        db.metadata.create_all(db.engine)
        services = Service.query.all()
        staff_role = Role.query.filter_by(name='Staff').first()

        print 'Enter full name: '
        full_name = raw_input()
        print 'Enter email address: '
        email = raw_input()
        print 'Enter phone number: '
        phone_number = raw_input()
        print 'Current organizations:'
        for service in services:
            print '%d %s' % (service.id, service.name)
        print 'Enter the id of the organization to associate with this user: '
        service_id = raw_input()
        print 'Is this a staff user? Enter y or n: '
        staff_user_yn = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = AppUser(
            email=email,
            password=encrypt_password(password),
            service_id=service_id,
            full_name=full_name,
            phone_number=phone_number
        )
        db.session.add(user)
        if staff_user_yn == 'y':
            user.roles.append(staff_role)
        db.session.commit()
        print 'User added.'

if __name__ == '__main__':
    sys.exit(main())
