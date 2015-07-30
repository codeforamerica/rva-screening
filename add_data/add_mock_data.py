#!/usr/bin/env python
import sys
import random

from faker import Factory
from faker.providers import BaseProvider
from flask import current_app
from flask.ext.login import current_user, login_user, logout_user

from app import create_app, bcrypt
from app.example_data import (
  RELATIONSHIPS,
  ADDRESS_TYPES,
  PHONE_TYPES,
  REFERRAL_STATUSES
)
from app.models import (
  AppUser,
  Service,
  SlidingScale,
  Patient,
  PhoneNumber,
  Address,
  EmergencyContact,
  IncomeSource,
  HouseholdMember,
  Employer,
  PatientReferral,
  PatientScreeningResult,
  db
)
from app.template_constants import *
import clear_db
import add_service_data

def choice(array):
  return fake.random_element(array)[0]

def formatted_phone_number():
  return (
    "(%s%s%s) %s%s%s-%s%s%s%s"
    % tuple(str(fake.random_digit_not_null()) for x in range(10))
  )

class PatientProvider(BaseProvider):

  def some(self, generator_name, amt_range=(1,3)):
    amt = random.randint(*amt_range)
    if amt:
      return [getattr(self, generator_name)() for i in range(amt)]
    else:
      return []

  def screening_results(self, sliding_scale_ids):
    return PatientScreeningResult(
      service_id = current_user.service_id,
      sliding_scale_id = (
        fake.random_element(sliding_scale_ids)
        if sliding_scale_ids
        else None
      ), 
      eligible_yn = choice(YN_NONULL_CHOICES),
      notes = fake.text(max_nb_chars=200)
    )

  def referrals(self, service_ids):
    return PatientReferral(
      to_service_id = fake.random_element(service_ids),
      from_app_user_id = current_user.id,
      status = fake.random_element(REFERRAL_STATUSES),
      notes = fake.text(max_nb_chars=200) 
    )

  def patient(self):
    return Patient(
      first_name = fake.first_name(),
      last_name = fake.last_name(),
      dob = fake.date_time_between(start_date="-110y", end_date="now").date(),
      ssn = fake.ssn(),

      email = fake.email(),
      has_transport_yn = choice(YN_CHOICES),

      gender = choice(GENDER_CHOICES),
      transgender = choice(TRANSGENDER_CHOICES),
      race = choice(RACE_CHOICES),
      ethnicity = choice(ETHNICITY_CHOICES),
      language = choice(LANGUAGE_CHOICES),
      has_interpreter_yn = choice(YNNA_CHOICES),
      education_level = 'High school',
      marital_status = choice(MARITAL_STATUS_CHOICES),
      veteran_yn = choice(YN_CHOICES),
      housing_status = choice(HOUSING_STATUS_CHOICES),
      years_living_in_area = fake.random_int(min=0, max=20),
      months_living_in_area = fake.random_int(min=0, max=11),
      #city_or_county_of_residence = 'Richmond',
      temp_visa_yn = choice(YN_CHOICES),

      student_status = choice(STUDENT_STATUS_CHOICES),
      employment_status = choice(EMPLOYMENT_STATUS_CHOICES),
      spouse_employment_status = choice(EMPLOYMENT_STATUS_CHOICES),
      years_unemployed = fake.random_int(min=0, max=5),
      months_unemployed = fake.random_int(min=0, max=11),
      spouse_years_unemployed = fake.random_int(min=0, max=5),
      spouse_months_unemployed = fake.random_int(min=0, max=11),

      #last_healthcare = '2 years ago.',
      insurance_status = choice(YN_CHOICES),
      coverage_type = choice(COVERAGE_TYPE_CHOICES),
      has_prescription_coverage_yn = choice(YNN_NONULL_CHOICES),
      has_vcc = choice(YN_CHOICES),
      eligible_insurance_types = choice(COVERAGE_ELIGIBILITY_CHOICES),
      applied_for_vets_benefits_yn = choice(YNNA_CHOICES),
      eligible_for_vets_benefits_yn = choice(YNN_NONULL_CHOICES),
      applied_for_medicaid_yn = choice(YN_CHOICES),
      #medicaid_date_effective
      applied_for_ssd_yn = choice(YN_CHOICES),
      #ssd_date_effective
      care_due_to_accident_yn = choice(YN_CHOICES),
      accident_work_related_yn = choice(YN_CHOICES),

      filed_taxes_yn = choice(YN_CHOICES),
      claimed_as_dependent_yn = choice(YNN_CHOICES),
      #how_food_and_shelter
      #how_other_expenses
    )

  def phone_numbers(self):
    return PhoneNumber(
      phone_number = formatted_phone_number(),
      number_description = fake.random_element(PHONE_TYPES),
    )

  def household_members(self):
    return HouseholdMember(
      full_name = fake.name(),
      dob = fake.date_time_between(start_date="-110y", end_date="now").date(),
      ssn = fake.ssn(),
      relationship = fake.random_element(RELATIONSHIPS)
    )

  def income_sources(self):
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
      monthly_amount=fake.random_int(100, 2000)
    )

  def emergency_contacts(self):
    return EmergencyContact(
      full_name = fake.name(),
      relationship = fake.random_element(RELATIONSHIPS),
      phone_number = formatted_phone_number()
    )

  def addresses(self):
    return Address(
      address1 = fake.street_address(),
      city = fake.city(),
      state = choice(STATE_CHOICES),
      zip_code = fake.postcode(),
      address_description = fake.random_element(ADDRESS_TYPES)
    )

  def employers(self):
    return Employer(
      employer_name = fake.company(),
      phone_number = formatted_phone_number(),
      employee = choice(EMPLOYEE_CHOICES),
      start_date = fake.date_time_between(start_date="-10y", end_date="now").date()
    )

def add_users(services):
  for service in services:
    user = AppUser(
      email = service.name.lower().replace(' ', '_') + '_user@test.com',
      password = bcrypt.generate_password_hash('password'),
      service_id = service.id,
      full_name = fake.name(),
      phone_number = formatted_phone_number()
    )
    db.session.add(user)
  db.session.commit()
  app_users = AppUser.query.all()

  print "Added users"
  return app_users


def add_patients(app_users, services):
  many_to_one_field_counts = {
    'phone_numbers': [0,4],
    'household_members': [0,5],
    'income_sources': [0,4],
    'emergency_contacts': [0,2],
    'addresses': [0,2],
    'employers': [0,2],
  }

  with current_app.test_request_context():
    for _ in range(50):
      login_user(fake.random_element(app_users))
      patient = fake.patient()
      for field in many_to_one_field_counts:
        objs = fake.some(field, many_to_one_field_counts[field])
        for obj in objs:
          getattr(patient, field).append(obj)
      db.session.add(patient)
      db.session.commit()
      for _ in range(random.randint(0,3)):
        login_user(fake.random_element(app_users))
        possible_service_ids = [s.id for s in services if s.id != current_user.service_id]
        patient.referrals.append(fake.referrals(possible_service_ids))
        logout_user()
      for _ in range(random.randint(0,3)):
        login_user(fake.random_element(app_users))
        possible_sliding_scale_ids = [s.id for s in SlidingScale.query.filter(
          SlidingScale.service_id == current_user.service_id
        )]
        patient.screening_results.append(fake.screening_results(possible_sliding_scale_ids))
        logout_user()
      db.session.commit()

  print "Added patients with lots of data, referrals and screening results"


fake = Factory.create('en_US')
fake.add_provider(PatientProvider)


def main():
  app = create_app()

  with app.app_context():
    # Remove all existing data in database
    clear_db.main(app)

    # Add services, with locations, screening criteria, and sliding scales
    services = add_service_data.main(app)

    # Add several users, associated with different services
    services = Service.query.all()
    app_users = add_users(services)

    # Add patients with lots of data, referrals, and screening results
    add_patients(app_users, services)

    # Yay!
    print (
      'All done!\n\n'
      'User accounts are:'
    )
    for user in app_users:
      print user.email

    print '\nPasswords for all are \'password\'.'


if __name__ == '__main__':
  sys.exit(main())


