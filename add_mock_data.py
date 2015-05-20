from faker import Factory
from faker.providers import BaseProvider

from app import app, bcrypt
from app.models import User, db

class PatientProvider(BaseProvider):

    patients = 100
    chance_of_1_address = 0.8
    chance_of_2_addresses = 0.2
    chance_of_3_addresses = 0.05
    chance_of_phone = 0.9
    chance_of_2_phones = 0.3
    chance_of_3_phones = 0.1
    chance_of_email = 0.15
    age_range = [9, 85]

    def patient(self):
        return None

    def phone_numbers(self):
        return None

    def addresses(self):
        return None

    def household_members(self):
        return None

    def income_sources(self):
        return None

    def emergency_contacts(self):
        return None

    def address(self):
        return None

fake = Factory.create('en_US')
names = [fake.name() for i in range(100)]

print names[:10]

