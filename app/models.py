from app import db

class Patient(db.Model):
  # Basic ID
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(128))
  first_name = db.Column(db.String(64))
  middle_name = db.Column(db.String(64))
  last_name = db.Column(db.String(64))
  dob = db.Column(db.Date())
  ssn = db.Column(db.String(11))

  # Contact
  email = db.Column(db.String(64))
  phone_numbers = db.relationship('PhoneNumber', backref='patient', lazy='dynamic')
  addresses = db.relationship('Address', backref='patient', lazy='dynamic')
  emergency_contacts = db.relationship('EmergencyContact', backref='patient', lazy='dynamic')

  # Demographic/social history
  gender = db.Column(db.String(2))
  transgender = db.Column(db.String(3))
  race = db.Column(db.String(16))
  ethnicity = db.Column(db.String(32))
  languages = db.Column(db.String(64))
  has_interpreter_yn = db.Column(db.String(1))
  education_level = db.Column(db.String(16))
  marital_status = db.Column(db.String(16))
  veteran_yn = db.Column(db.String(1))
  housing_status = db.Column(db.String(16))
  months_living_in_area = db.Column(db.Integer)
  temp_visa_yn = db.Column(db.String(1))
  has_transport_yn = db.Column(db.String(1))

  # Employment
  student_status = db.Column(db.String(16))
  employment_status = db.Column(db.String(16))
  months_unemployed = db.Column(db.Integer)
  employment_changes = db.Column(db.String(32))
  spouse_employment_status = db.Column(db.String(16))
  spouse_months_unemployed = db.Column(db.Integer)
  spouse_employment_changes = db.Column(db.String(16))
  employers = db.relationship('Employer', backref='patient', lazy='dynamic')

  # Healthcare/coverage
  last_healthcare = db.Column(db.String(128))
  insurance_status = db.Column(db.String(32))
  coverage_type = db.Column(db.String(32))
  insurances = db.relationship('Insurance', backref='patient', lazy='dynamic')
  has_prescription_coverage_yn = db.Column(db.String(1))
  has_pcp_yn = db.Column(db.String(1))
  has_psychiatrist_yn = db.Column(db.String(1))
  wants_psychiatrist_yn = db.Column(db.String(1))
  eligible_insurance_types = db.Column(db.String(64))
  applied_for_vets_benefits_yn = db.Column(db.String(1))
  eligible_for_vets_benefits_yn = db.Column(db.String(1))
  applied_for_medicaid_yn = db.Column(db.String(1))
  denied_medicaid_yn = db.Column(db.String(1))
  medicaid_date_effective = db.Column(db.Date())
  applied_for_ssd_yn = db.Column(db.String(1))
  ssd_date_effective = db.Column(db.Date())
  care_due_to_accident_yn = db.Column(db.String(1))
  accident_work_related_yn = db.Column(db.String(1))
  recently_lost_insurance_yn = db.Column(db.String(1))

  # Income/finances
  document_images = db.relationship('DocumentImage', backref='patient', lazy='dynamic')
  income_sources = db.relationship('IncomeSource', backref='patient', lazy='dynamic')
  household_members = db.relationship('HouseholdMember', backref='patient', lazy='dynamic')
  head_of_household_yn = db.Column(db.String(1))
  filed_taxes_yn = db.Column(db.String(1))
  claimed_as_dependent_yn = db.Column(db.String(1))
  how_food_and_shelter = db.Column(db.String(128))
  how_other_expenses = db.Column(db.String(128))
  total_annual_income = 0
  fpl_percentage = 0

  def __init__(self, **fields):
    self.__dict__.update(fields)

class PhoneNumber(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  phone_number = db.Column(db.String(32))
  description = db.Column(db.String(64))
  primary_yn = db.Column(db.String(1))

class Address(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  address1 = db.Column(db.String(64))
  address2 = db.Column(db.String(64))
  city = db.Column(db.String(64))
  state = db.Column(db.String(2))
  zip = db.Column(db.String(10))
  description = db.Column(db.String(64))

class EmergencyContact(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  name = db.Column(db.String(64))
  relationship = db.Column(db.String(64))
  phone_number = db.Column(db.String(32))

class HouseholdMember(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patientid = db.Column(db.Integer, db.ForeignKey("patient.id"))
  full_name = db.Column(db.String(64))
  dob = db.Column(db.Date())
  ssn = db.Column(db.String(11))
  relationship = db.Column(db.String(32))

class IncomeSource(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patientid = db.Column(db.Integer, db.ForeignKey("patient.id"))
  source = db.Column(db.String(64))
  annual_amount = db.Column(db.Integer)

class Employer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patientid = db.Column(db.Integer, db.ForeignKey("patient.id"))
  name = db.Column(db.String(64))
  phone_number = db.Column(db.String(32))
  employee = db.Column(db.String(16))
  start_date = db.Column(db.Date())

class DocumentImage(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  file_name = db.Column(db.String(64))
  description = db.Column(db.String(64))

class Insurance(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
  type = db.Column(db.String(32))

class Service(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64))
  password = db.Column(db.String(128))
  authenticated = db.Column(db.Boolean, default=False)
  service_id = db.Column(db.Integer, db.ForeignKey("service.id"))

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.email


