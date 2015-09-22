from flask.ext.security.utils import encrypt_password
from app.models import AppUser, Service, Patient, Role
from app import db


def insert_roles():
    Role.insert_roles()


def get_user():
    existing_user = AppUser.query.filter(
        AppUser.email == 'richmond@codeforamerica.org'
    ).first()
    if not existing_user:
        return insert_user()

    return existing_user


def insert_user():
    insert_roles()
    service = get_service()
    staff_role = Role.query.filter_by(name='Staff').first()
    app_user = AppUser(
        full_name='App User',
        email='richmond@codeforamerica.org',
        password=encrypt_password('password'),
        service=service
    )
    db.session.add(app_user)
    app_user.roles.append(staff_role)
    db.session.commit()
    return app_user


def get_service():
    existing_service = Service.query.first()
    if not existing_service:
        return insert_service()
    return existing_service


def insert_service():
    service = Service(
        name='Richmond Clinic'
    )
    db.session.add(service)
    db.session.commit()
    return service


def get_patient():
    existing_patient = Patient.query.first()
    if not existing_patient:
        return insert_patient()
    return existing_patient


def insert_patient():
    patient = Patient(
        first_name='John',
        last_name='Richmond',
        dob='1950-01-01',
        ssn='111-11-1111'
    )
    db.session.add(patient)
    db.session.commit()
    return patient
