from app import db
import datetime
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from sqlalchemy import event, DDL, Table
from sqlalchemy.dialects.postgresql import ARRAY, HSTORE
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

class BasicTable(object):
  created = db.Column(db.DateTime)
  last_modified = db.Column(db.DateTime)

  @declared_attr
  def created_by_id(cls):
    return db.Column(
      db.Integer,
      db.ForeignKey("app_user.id", use_alter = True, name='fk_created_by_id')
    )

  @declared_attr
  def created_by(cls):
    return db.relationship(
      "AppUser",
      foreign_keys=lambda: cls.created_by_id
    )

  @declared_attr
  def last_modified_by_id(cls):
    return db.Column(
      db.Integer,
      db.ForeignKey("app_user.id", use_alter = True, name='fk_last_modified_by_id')
    )

  @declared_attr
  def last_modified_by(cls):
    return db.relationship(
      "AppUser",
      foreign_keys=lambda: cls.last_modified_by_id
    )


class ActionLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  transaction_id = db.Column(db.Integer)
  action_timestamp = db.Column(db.DateTime())
  table_name = db.Column(db.String(64))
  row_id = db.Column(db.Integer)
  app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"))
  app_user = relationship("AppUser")
  action = db.Column(db.String(1))
  row_data = db.Column(HSTORE)
  changed_fields = db.Column(HSTORE)


class AppUser(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64))
  password = db.Column(db.String(128))
  authenticated = db.Column(db.Boolean, default=False)
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
  full_name = db.Column(db.String(64))
  phone_number = db.Column(db.String(32))

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.email


class Patient(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)

  # Basic ID
  full_name = db.Column(db.String(128), info=_('Full name'))
  first_name = db.Column(db.String(64), info=_('First name'))
  middle_name = db.Column(db.String(64), info=_('Middle name'))
  last_name = db.Column(db.String(64), info=_('Last name'))
  dob = db.Column(db.Date(), info=_('DOB'))
  ssn = db.Column(db.String(11), info=_('SSN'))

  # Contact
  email = db.Column(db.String(64), info=_('Email address'))
  phone_numbers = db.relationship('PhoneNumber', backref='patient', lazy='dynamic')
  addresses = db.relationship('Address', backref='patient', lazy='dynamic')
  emergency_contacts = db.relationship('EmergencyContact', backref='patient', lazy='dynamic')

  # Demographic/social history
  gender = db.Column(db.String(2), info=_('Gender'))
  transgender = db.Column(db.String(3), info=_('Transgender'))
  race = db.Column(db.String(16), info=_('Race'))
  race_other = db.Column(db.String(32), info=_('Race - Other'))
  ethnicity = db.Column(db.String(32), info=_('Ethnicity'))
  languages = db.Column(db.String(64), info=_('Languages spoken'))
  languages_other = db.Column(db.String(64), info=_('Languages - Other'))
  has_interpreter_yn = db.Column(db.String(1), info=_('Has interpreter?'))
  education_level = db.Column(db.String(16), info=_('Education level'))
  marital_status = db.Column(db.String(16), info=_('Marital status'))
  veteran_yn = db.Column(db.String(1), info=_('US veteran?'))
  housing_status = db.Column(db.String(16), info=_('Housing status'))
  housing_status_other = db.Column(db.String(32), info=_('Housing status - Other'))

  years_living_in_area = db.Column(db.Integer, info=_('Years living in area'))
  months_living_in_area = db.Column(db.Integer, info=_('Months living in area'))
  city_or_county_of_residence = db.Column(db.String(64), info=_('City or County of Residence'))
  temp_visa_yn = db.Column(db.String(1), info=_('Temporary visa?'))
  has_transport_yn = db.Column(db.String(1), info=_('Has transportation?'))

  # Employment
  student_status = db.Column(db.String(16), info=_('Are you currently a student?'))
  employment_status = db.Column(db.String(16), info=_('Employment status'))
  years_unemployed = db.Column(db.Integer, info=_('Years unemployed'))
  months_unemployed = db.Column(db.Integer, info=_('Months unemployed'))
  employment_changes = db.Column(db.String(32), info=_('Employment changes'))
  spouse_employment_status = db.Column(db.String(16), info=_('Spouse\'s employment status'))
  spouse_years_unemployed = db.Column(db.Integer, info=_('Spouse\'s years unemployed'))
  spouse_months_unemployed = db.Column(db.Integer, info=_('Spouse\'s months unemployed'))
  spouse_employment_changes = db.Column(db.String(16), info=_('Spouse\'s employment changes'))
  employers = db.relationship('Employer', backref='patient', lazy='dynamic')
  years_at_current_employer = db.Column(db.Integer, info=('Years at current employer'))
  spouse_years_at_current_employer = db.Column(db.Integer, info=('Spouse\'s years at current employer'))

  # Healthcare/coverage
  last_healthcare = db.Column(db.String(128), info=_('Last healthcare received'))
  insurance_status = db.Column(db.String(32), info=_('Insurance status'))
  coverage_type = db.Column(db.String(32), info=_('Coverage type'))
  coverage_type_other = db.Column(db.String(32), info=_('Coverage type - Other'))
  has_prescription_coverage_yn = db.Column(db.String(1), info=_('Has prescription coverage?'))
  has_vcc = db.Column(db.String(1), info=_('Has VCC Card?'))
  has_pcp_yn = db.Column(db.String(1), info=_('Has primary care provider?'))
  has_psychiatrist_yn = db.Column(db.String(1), info=_('Has psychiatrist?'))
  wants_psychiatrist_yn = db.Column(db.String(1), info=_('Wants psychiatrist?'))
  eligible_insurance_types = db.Column(db.String(64), info=_('Eligible insurance types'))
  applied_for_vets_benefits_yn = db.Column(db.String(1), info=_('Applied for veteran benefits?'))
  eligible_for_vets_benefits_yn = db.Column(db.String(1), info=_('Eligible for veteran benefits?'))
  applied_for_medicaid_yn = db.Column(db.String(1), info=_('Applied for Medicaid?'))
  denied_medicaid_yn = db.Column(db.String(1), info=_('Denied Medicaid?'))
  medicaid_date_effective = db.Column(db.Date(), info=_('Medicaid effective date'))
  applied_for_ssd_yn = db.Column(db.String(1), info=_('Applied for SSD?'))
  ssd_date_effective = db.Column(db.Date(), info=_('SSD date effective'))
  care_due_to_accident_yn = db.Column(db.String(1), info=_('Seeking care due to accident?'))
  accident_work_related_yn = db.Column(db.String(1), info=_('Accident work-related?'))
  recently_lost_insurance_yn = db.Column(db.String(1), info=_('Recently lost insurance?'))

  # Income/finances
  document_images = db.relationship('DocumentImage', backref='patient', lazy='dynamic')
  income_sources = db.relationship('IncomeSource', backref='patient', lazy='dynamic')
  household_members = db.relationship('HouseholdMember', backref='patient', lazy='dynamic')
  head_of_household_yn = db.Column(db.String(1), info=_('Head of household?'))
  filed_taxes_yn = db.Column(db.String(1), info=_('Filed taxes last year?'))
  claimed_as_dependent_yn = db.Column(db.String(1), info=_('Claimed as dependent?'))
  how_food_and_shelter = db.Column(db.String(128), info=_('How do you get food and shelter?'))
  how_other_expenses = db.Column(db.String(128), info=_('How do you pay other expenses?'))
  total_annual_income = 0
  fpl_percentage = 0

  # Permissions
  patient_service_permissions = db.relationship('PatientServicePermission', backref='patient', lazy='dynamic')
  services = db.relationship('Service', secondary='patient_service_permission')

  referrals = db.relationship('PatientReferral', backref='patient', lazy='dynamic')

  def __init__(self, **fields):
    self.__dict__.update(fields)

  def update_stats(self):
    self.total_annual_income = sum(
      source.monthly_amount * 12 for source in self.income_sources if source.monthly_amount
    )
    self.fpl_percentage = (
      float(self.total_annual_income) / 
      (5200 * int(self.household_members.count() + 1) + 9520)) * 100


class PhoneNumber(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  phone_number = db.Column(db.String(32), info=_('Phone number'))
  number_description = db.Column(db.String(64), info=_('Description'))
  primary_yn = db.Column(db.String(1), info=_('Primary number?'))


class Address(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  address1 = db.Column(db.String(64), info=_('Address 1'))
  address2 = db.Column(db.String(64), info=_('Address 2'))
  city = db.Column(db.String(64), info=_('City'))
  state = db.Column(db.String(2), info=_('State'))
  zip_code = db.Column(db.String(10), info=_('ZIP'))
  address_description = db.Column(db.String(64), info=_('Description'))


class EmergencyContact(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  full_name = db.Column(db.String(64), info=_('Full name'))
  relationship = db.Column(db.String(64), info=_('Relationship to patient'))
  phone_number = db.Column(db.String(32), info=_('Phone number'))


class HouseholdMember(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  full_name = db.Column(db.String(64), info=_('Full name'))
  dob = db.Column(db.Date(), info=_('DOB'))
  ssn = db.Column(db.String(11), info=_('SSN'))
  relationship = db.Column(db.String(32), info=_('Relationship to patient'))


class IncomeSource(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  source = db.Column(db.String(64), info=_('Source'))
  monthly_amount = db.Column(db.Integer, info=_('Monthly amount'))


class Employer(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  employer_name = db.Column(db.String(64), info=_('Name'))
  phone_number = db.Column(db.String(32), info=_('Phone number'))
  employee = db.Column(db.String(16), info=_('Employee'))
  start_date = db.Column(db.Date(), info=_('Start date'))


class DocumentImage(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  file_name = db.Column(db.String(64))
  file_description = db.Column(db.String(64), info=_('Description'))


class PatientReferral(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  from_app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"))
  to_service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
  status = db.Column(db.String(9), info=_('Status'))
  notes = db.Column(db.Text, info=_('Notes'))


class Service(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  description = db.Column(db.Text)
  logo_url = db.Column(db.String(128))
  website_url = db.Column(db.String(128))
  main_contact_name = db.Column(db.String(64))
  main_contact_phone = db.Column(db.String(32))
  fpl_cutoff = db.Column(db.Integer)
  uninsured_only_yn = db.Column(db.String(1))
  medicaid_ineligible_only_yn = db.Column(db.String(1))
  residence_requirement_yn = db.Column(db.String(1))
  time_in_area_requirement_yn = db.Column(db.String(1))
  sliding_scales = db.relationship('SlidingScale', backref='service', lazy='dynamic')
  locations = db.relationship('ServiceLocation', backref='service', lazy='dynamic')
  users = db.relationship('AppUser', primaryjoin='Service.id==AppUser.service_id', backref='service')
  translations = db.relationship('ServiceTranslation', backref='service', lazy='dynamic')


class ServiceTranslation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
  language_code = db.Column(db.String(16))
  description = db.Column(db.Text)


class ServiceLocation(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
  name = db.Column(db.String(64))
  contact_name = db.Column(db.String(64))
  phone_number = db.Column(db.String(32))
  address = db.Column(db.String(64))
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)


class SlidingScale(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
  scale_name = db.Column(db.String(64))
  fpl_low = db.Column(db.Float)
  fpl_high = db.Column(db.Float)
  sliding_scale_fees = db.relationship('SlidingScaleFee', backref='slidingscale', lazy='dynamic')


class SlidingScaleFee(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sliding_scale_id = db.Column(db.Integer, db.ForeignKey("sliding_scale.id"))
  name = db.Column(db.String(128))
  price_absolute = db.Column(db.Integer)
  price_percentage = db.Column(db.Integer)


class PatientServicePermission(BasicTable, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))


@event.listens_for(BasicTable, 'before_insert', propagate=True)
def before_insert(mapper, connection, instance):
  instance.created = datetime.datetime.utcnow()
  instance.created_by_id = current_user.id if hasattr(current_user, 'id') else None

@event.listens_for(BasicTable, 'before_update', propagate=True)
def before_update(mapper, connection, instance):
  instance.last_modified = datetime.datetime.utcnow()
  instance.last_modified_by_id = current_user.id if hasattr(current_user, 'id') else None


