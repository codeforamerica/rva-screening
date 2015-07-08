from faker import Factory
from faker.providers import BaseProvider
from datetime import date
import random

from app import app, bcrypt
from app.models import *

from app.example_data import (
        STATE_CHOICES,
        ETHNICITY_CHOICES,
        RACE_CHOICES,
        RELATIONSHIPS,
        ADDRESS_TYPES,
        PHONE_TYPES,
        GENDER_CHOICES,
        HOUSING_STATUS_CHOICES,
        MARITAL_STATUS_CHOICES,
        EMPLOYMENT_STATUS_CHOICES,
        YN_CHOICES,
        YNN_CHOICES,
        )


def choice(array):
    return fake.random_element(array)[0]


class PatientProvider(BaseProvider):

    def some(self, generator_name, amt_range=(1,3)):
        amt = random.randint(*amt_range)
        if amt:
            return [getattr(self, generator_name)() for i in range(amt)]
        else:
            return []

    def patient(self):
        p = Patient(
                full_name = fake.name(),
                dob = date(
                    fake.random_int(1930,2010),
                    int(fake.month()),
                    random.randint(1,26)
                    ),
                ssn = fake.ssn(),
                email = fake.email(),
                gender = fake.random_element(GENDER_CHOICES),
                race = choice(RACE_CHOICES),
                ethnicity = choice(ETHNICITY_CHOICES),
                marital_status = choice(MARITAL_STATUS_CHOICES),
                veteran_yn = choice(YN_CHOICES),
                housing_status = choice(HOUSING_STATUS_CHOICES),
                employment_status = choice(EMPLOYMENT_STATUS_CHOICES),
            )

        return p

    def phone(self):
        return PhoneNumber(
                phone_number = fake.phone_number(),
                description = fake.random_element(PHONE_TYPES),
                )

    def household_member(self):
        return HouseholdMember(
                full_name = fake.name(),
                relationship = fake.random_element(
                    RELATIONSHIPS
                    )
                )

    def income_source(self):
        return IncomeSource(
                source = fake.random_element((
                    fake.company(),
                    "food stamps",
                    "child support",
                    "disability",
                    "ssi",
                    "retirement",
                    "self-employment",
                    )),
                annual_amount=fake.random_int(100, 5000)
                )

    def emergency_contact(self):
        return EmergencyContact(
                name = fake.name(),
                relationship = fake.random_element(RELATIONSHIPS),
                phone_number = fake.phone_number()
                )

    def address(self):
        return Address(
                address1 = fake.street_address(),
                city = fake.city(),
                state = choice(STATE_CHOICES),
                zip = fake.postcode(),
                description = fake.random_element(ADDRESS_TYPES)
                )

    def employer(self):
        return Employer(
                name = fake.company(),
                phone_number = fake.phone_number()
                )
fake = Factory.create('en_US')
fake.add_provider(PatientProvider)

amounts = {
        'phone': [0,4],
        'household_member': [0,5],
        'income_source': [0,4],
        'emergency_contact': [0,2],
        'address': [0,2],
        'employer': [0,2],
        }

attributes = {
        'phone': 'phone_numbers',
        'household_member': 'household_members',
        'income_source': 'income_sources',
        'emergency_contact': 'emergency_contacts',
        'address': 'addresses',
        'employer': 'employers',
        }


def save_lots_of_patients_and_things(db, num_patients=50):
    for i in range(num_patients):
        p = fake.patient()
        db.session.add(p)
        for thing in amounts:
            objs = fake.some(thing, amounts[thing])
            for obj in objs:
                getattr(p, attributes[thing]).append(obj)
                db.session.add(obj)
        db.session.commit()

def run():
    with app.app_context():
        db.metadata.create_all(db.engine)
        save_lots_of_patients_and_things(db)

if __name__ == '__main__':
    run()


