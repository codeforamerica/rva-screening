import re
from app import template_constants as CONSTANTS
from flask import current_app, request
from flask.ext.babel import gettext as _
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import widgets, fields, validators
from wtforms import Form as NoCsrfForm
from wtforms.validators import DataRequired, Email, ValidationError, Optional

ALL_INTEGERS = re.compile('[^\d.]')
def validate_digit_count(form, field, count):
    # Strips out non-integer characters, checks whether number of digits
    # matches expectation
    if field.data:
        value = re.sub(ALL_INTEGERS, '', field.data)
        return len(value) == count or len(value) == 0

def validate_ssn(form, field):
  if validate_digit_count(form, field, 9) is False:
    raise ValidationError('Social security number should be 9 digits.')

def validate_phone_number(form, field):
  if validate_digit_count(form, field, 10) is False:
    raise ValidationError('Phone number should be 10 digits.')

class PrescreenForm(Form):
  household_size = fields.IntegerField(
    _('What is your household size?'),
    validators=[]
  )
  household_income = fields.IntegerField(
    _('What is your monthly household income?'),
    validators=[]
  )
  has_health_insurance = fields.RadioField(
    _('Do you have health insurance?'),
    choices = CONSTANTS.YNN_NONULL_CHOICES,
    default = "",
  )
  eligible_for_medicaid = fields.RadioField(
    _('Are you eligible for Medicare/Medicaid?'),
    choices = CONSTANTS.YNN_NONULL_CHOICES,
    default = "",
  ) 

class PhoneNumberForm(NoCsrfForm):
  phone_number = fields.TextField(
    _('Phone number'),
    [Optional(), validators.Length(max=32), validate_phone_number]
  )
  number_description = fields.TextField(
    _('Description'),
    [Optional(), validators.Length(max=64)]
  )

class AddressForm(NoCsrfForm):
  address1 = fields.TextField(_('Address'), [Optional(), validators.Length(max=64)])
  address2 = fields.TextField([Optional(), validators.Length(max=64)])
  city = fields.TextField(_('City'), [Optional(), validators.Length(max=64)])
  state = fields.SelectField(
    _('State'),
    choices = CONSTANTS.STATE_CHOICES,
    default = "VA",
  )
  zip_code = fields.TextField(_('ZIP'), [Optional(), validators.Length(max=10)])
  address_description = fields.TextField(
    _('What kind of address is this?'),
    [Optional(), validators.Length(max=64)]
  )

class EmergencyContactForm(NoCsrfForm):
  full_name = fields.TextField(_('Name'), [Optional(), validators.Length(max=64)])
  relationship = fields.TextField(
    _('Relationship to patient'),
    [Optional(), validators.Length(max=64)]
  )
  phone_number = fields.TextField(
    _('Phone number'),
    [Optional(), validators.Length(max=32), validate_phone_number]
  )

class HouseholdMemberForm(NoCsrfForm):
  full_name = fields.TextField(
    _('Full name'),
    [Optional(), validators.Length(max=64)]
  )
  dob = fields.DateField(
    _('Date of birth'),
    validators=[Optional()]
  )
  ssn = fields.TextField(
    _('Social security number'),
    [Optional(), validators.Length(max=11), validate_ssn]
  )
  relationship = fields.TextField(
    _('Relationship to patient'),
    [Optional(), validators.Length(max=32)]
  )

class IncomeSourceForm(NoCsrfForm):
  source = fields.TextField(_('Source'), [Optional(), validators.Length(max=64)])
  monthly_amount = fields.DecimalField(_('Monthly amount'), validators=[Optional()])


class EmployerForm(NoCsrfForm):
  employer_name = fields.TextField(
    _('Employer name'),
    [Optional(), validators.Length(max=64)]
  )
  phone_number = fields.TextField(
    _('Phone number'),
    [Optional(), validators.Length(max=32), validate_phone_number]
  )
  employee = fields.SelectField(
    _('Whose job?'),
    choices = CONSTANTS.EMPLOYEE_CHOICES,
    default = _('Patient')
  )
  start_date = fields.DateField(_('Start date'), validators=[Optional()])

class DocumentImageForm(NoCsrfForm):
  id = fields.IntegerField()
  created = fields.TextField()
  created_by = fields.TextField()
  file_name = FileField(
    validators=[FileAllowed(
      ['jpg', 'png', 'pdf'],
      'Allowed file types are .jpg, .png, and .pdf'
    )]
  )
  file_description = fields.TextField(
    _('Description'),
    [Optional(), validators.Length(max=64)]
  )

class PatientForm(Form):
  ### Basic ID
  full_name = fields.TextField(
    _('Full legal name'),
    validators=[DataRequired(), validators.Length(max=128)])
  first_name = fields.TextField(_('First name'))
  middle_name = fields.TextField(_('Middle name'))
  last_name = fields.TextField(_('Last name'))
  dob = fields.DateField(_('Date of birth'))
  ssn = fields.TextField(
    _('Social security number'),
    [Optional(), validators.Length(max=11), validate_ssn]
  )

  ### Contact
  email = fields.TextField(
    _('Email address'),
    validators=[Optional(), Email(), validators.Length(max=64)]
  )
  phone_numbers = fields.FieldList(fields.FormField(
    PhoneNumberForm
  ), min_entries=1)
  addresses = fields.FieldList(fields.FormField(
    AddressForm
  ))
  emergency_contacts = fields.FieldList(fields.FormField(
    EmergencyContactForm
  ))

  ### Demographic/social history
  gender = fields.SelectField(
    _('Gender'),
    choices = CONSTANTS.GENDER_CHOICES,
    default = _('No answer')
  )
  transgender = fields.SelectField(
    _('Transgender'),
    choices = CONSTANTS.TRANSGENDER_CHOICES,
    default = "",
  )
  race = fields.SelectField(
    _('Race'),
    choices = CONSTANTS.RACE_CHOICES,
    default = "",
  )
  race_other = fields.TextField(
    _('Please specify other race'),
    [Optional(), validators.Length(max=32)]
  )
  ethnicity = fields.SelectField(
    _('Ethnicity'),
    choices = CONSTANTS.ETHNICITY_CHOICES,
    default = "",
  )
  languages = fields.SelectMultipleField(
    _('Language'),
    choices = CONSTANTS.LANGUAGE_CHOICES,
    default = "",
  )
  languages_other = fields.TextField(
    _('Please specify other languages'),
    [Optional(), validators.Length(max=64)]
  )
  # has_interpreter_yn = fields.BooleanField(_(''))
  # has_interpreter_yn = db.Column(db.String(1), info='Has interpreter?')
  # education_level = db.Column(db.String(16), info='Education level')
  marital_status = fields.SelectField(
    _('Marital status'),
    choices = CONSTANTS.MARITAL_STATUS_CHOICES,
    default = "",
  )
  veteran_yn = fields.SelectField(
    _('Are you a veteran of the United States?'),
    choices = CONSTANTS.YN_CHOICES,
    default = "",
  )  
  housing_status = fields.SelectField(
    _('Living situation'),
    choices = CONSTANTS.HOUSING_STATUS_CHOICES,
    default = "",
  )
  housing_status_other = fields.TextField(
    _('Please specify other living situation'),
    [Optional(), validators.Length(max=32)]
  )
  # housing_status = db.Column(db.String(16), info='Housing status')
  # months_living_in_area = db.Column(db.Integer, info='Months living in area')
  # temp_visa_yn = db.Column(db.String(1), info='Temporary visa?')
  # has_transport_yn = db.Column(db.String(1), info='Has transportation?')

  ### Employment
  # student_status = db.Column(db.String(16), info='Are you currently a student?')
  student_status = fields.SelectField(
    _('Student status'),
    choices = CONSTANTS.STUDENT_STATUS_CHOICES,
    default = "",
  )
  employment_status = fields.SelectField(
    _('Employment status'),
    choices = CONSTANTS.EMPLOYMENT_STATUS_CHOICES,
    default = "",
  )
  spouse_employment_status = fields.SelectField(
    _('Spouse\'s employment status'),
    choices = CONSTANTS.EMPLOYMENT_STATUS_CHOICES,
    default = "",
  )
  # months_unemployed
  # employment_changes
  # spouse_months_unemployed
  # spouse_employment_changes
  employers = fields.FieldList(fields.FormField(
    EmployerForm
  ))

  ### Healthcare/coverage
  last_healthcare = fields.TextField(
    _('When and where did you last receive healthcare services?'),
    [Optional(), validators.Length(max=128)]
  )
  insurance_status = fields.SelectField(
    _('Do you have insurance or a card to help you cover medical costs?'),
    choices = CONSTANTS.YN_CHOICES,
    default = "",
  )
  coverage_type = fields.SelectField(
    _('Coverage type'),
    choices = CONSTANTS.COVERAGE_TYPE_CHOICES,
    default = "",
  )
  coverage_type_other = fields.TextField(
    _('Please specify other coverage type'),
    [Optional(), validators.Length(max=32)]
  )
  # has_prescription_coverage_yn
  # has_pcp_yn
  # has_psychiatrist_yn
  # wants_psychiatrist_yn
  # eligible_insurance_types
  # applied_for_vets_benefits_yn
  # eligible_for_vets_benefits_yn
  # applied_for_medicaid_yn
  # denied_medicaid_yn
  # medicaid_date_effective
  # applied_for_ssd_yn
  # ssd_date_effective
  # care_due_to_accident_yn
  # accident_work_related_yn
  # recently_lost_insurance_yn

  ### Income/finances
  document_images = fields.FieldList(fields.FormField(
    DocumentImageForm
  ))
  income_sources = fields.FieldList(fields.FormField(
    IncomeSourceForm
  ))
  household_members = fields.FieldList(fields.FormField(
    HouseholdMemberForm
  ))
  # head_of_household_yn
  # filed_taxes_yn
  # claimed_as_dependent_yn
  # how_food_and_shelter
  # how_other_expenses
