import re
from app import template_constants as CONSTANTS
from flask.ext.babel import gettext as _
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import fields, validators
from wtforms import Form as NoCsrfForm
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError, Optional


ALL_INTEGERS = re.compile('[^\d.]')


def validate_digit_count(form, field, count):
    """Strips out non-integer characters and checks whether number of digits
    matches expectation."""
    if field.data:
        value = re.sub(ALL_INTEGERS, '', field.data)
        return len(value) == count or len(value) == 0


def validate_ssn(form, field):
    """Checks that a social security number has 9 digits."""
    if validate_digit_count(form, field, 9) is False:
        raise ValidationError('Social security number should be 9 digits.')


def validate_phone_number(form, field):
    """Checks that a phone number is 10 digits"""
    if validate_digit_count(form, field, 10) is False:
        raise ValidationError('Phone number should be 10 digits.')


class RequiredIf(InputRequired):
    """A validator which makes a field required if another field
    is set and has a truthy value.
    http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
    """

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class ReferralCommentForm(Form):
    referral_id = fields.IntegerField()
    notes = fields.TextAreaField(
        _('Notes'),
        [Optional(), validators.Length(max=1000)]
    )
    submit = fields.SubmitField(
        _('Save')
    )

class ScreeningResultForm(Form):
    eligible_yn = fields.RadioField(
        _('Is this patient eligible for care at your organization?'),
        choices=CONSTANTS.YN_NONULL_CHOICES,
        default="N",
    )
    sliding_scale_id = fields.SelectField(
        _('Sliding Scale'),
        default=""
    )
    notes = fields.TextAreaField(
        _('Notes'),
        [Optional(), validators.Length(max=1000)]
    )
    submit = fields.SubmitField(
        _('Submit')
    )


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
        choices=CONSTANTS.YNN_NONULL_CHOICES,
        default="",
    )
    eligible_for_medicaid = fields.RadioField(
        _('Are you eligible for Medicare/Medicaid?'),
        choices=CONSTANTS.YNN_NONULL_CHOICES,
        default="",
    )

class SearchPatientForm(Form):
    search_patient_first_name = fields.TextField(
        _('First Name')
    )
    search_patient_last_name = fields.TextField(
        _('Last Name')
    )
    search_patient_dob = fields.DateField(
        _('Date of birth'),
        [Optional()]
    )
    search_patient_ssn = fields.TextField(
        _('Social security number'),
        [Optional(), validators.Length(max=11), validate_ssn]
    )


class PhoneNumberForm(NoCsrfForm):
    phone_number = fields.TextField(
        _('Phone number'),
        [Optional(), validators.Length(max=32), validate_phone_number]
    )
    number_description = fields.SelectField(
        _('Description'),
        choices=CONSTANTS.PHONE_DESCRIPTIONS,
        default="",
    )
    number_description_other = fields.TextField(_('Phone description - Other'), [Optional(), validators.Length(max=64)])


class AddressForm(NoCsrfForm):
    address1 = fields.TextField(_('Address'), [Optional(), validators.Length(max=64)])
    address2 = fields.TextField(_('Address Line 2'), [Optional(), validators.Length(max=64)])
    city = fields.TextField(_('City'), [Optional(), validators.Length(max=64)])
    state = fields.SelectField(
        _('State'),
        choices=CONSTANTS.STATE_CHOICES,
        default="VA",
    )
    zip_code = fields.TextField(_('ZIP'), [Optional(), validators.Length(max=10)])
    address_description = fields.SelectField(
        _('What kind of address is this?'),
        choices=CONSTANTS.ADDRESS_DESCRIPTIONS,
        default="",
    )
    address_description_other = fields.TextField(_('Address description - Other'), [Optional(), validators.Length(max=64)])


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
        choices=CONSTANTS.EMPLOYEE_CHOICES,
        default=_('Patient')
    )
    start_date = fields.DateField(_('Start date'), validators=[Optional()])


class DocumentImageForm(NoCsrfForm):
    file_name = FileField(
        validators=[FileAllowed(
            ['jpg', 'png', 'pdf'],
            'Allowed file types are .jpg, .png, and .pdf'
        )]
    )
    file_description = fields.TextField(
        _('Description'),
        [RequiredIf('file_name'), validators.Length(max=64)]
    )
    # The fields below aren't used for input, they just allow us to automatically
    # populate DocumentImage objects from the form object with populate_obj
    data_full = fields.HiddenField()
    data_large = fields.HiddenField()
    data_small = fields.HiddenField()


class PatientForm(Form):
    # BASIC ID
    # full_name will be deprecated soon
    full_name = fields.TextField(
        _('Full legal name'),
        validators=[Optional(), validators.Length(max=128)])
    first_name = fields.TextField(
        _('First name'),
        [DataRequired(), validators.Length(max=64)]
    )
    middle_name = fields.TextField(_('Middle name'), [validators.Length(max=64)])
    last_name = fields.TextField(
        _('Last name'),
        [DataRequired(), validators.Length(max=64)]
    )
    dob = fields.DateField(_('Date of birth'))
    ssn = fields.TextField(
        _('Social security number'),
        [Optional(), validators.Length(max=11), validate_ssn]
    )

    # CONTACT
    email = fields.TextField(
        _('Email address'),
        validators=[Optional(), Email(), validators.Length(max=64)]
    )
    phone_numbers = fields.FieldList(fields.FormField(
        PhoneNumberForm
    ))
    addresses = fields.FieldList(fields.FormField(
        AddressForm
    ))
    has_transport_yn = fields.SelectField(
        _("Do you have transportation?"),
        choices=CONSTANTS.YN_CHOICES,
        default="",
    )
    emergency_contacts = fields.FieldList(fields.FormField(
        EmergencyContactForm
    ))

    # DEMOGRAPHIC/SOCIAL HISTORY
    gender = fields.SelectField(
        _('Gender'),
        choices=CONSTANTS.GENDER_CHOICES,
        default="",
    )
    transgender = fields.SelectField(
        _('Transgender'),
        choices=CONSTANTS.TRANSGENDER_CHOICES,
        default="",
    )
    race = fields.SelectField(
        _('Race'),
        choices=CONSTANTS.RACE_CHOICES,
        default="",
    )
    race_other = fields.TextField(
        _('Please specify other race'),
        [Optional(), validators.Length(max=32)]
    )
    ethnicity = fields.SelectField(
        _('Ethnicity'),
        choices=CONSTANTS.ETHNICITY_CHOICES,
        default="",
    )
    ## testing out radio buttons in the general form
    languages = fields.SelectMultipleField(
        _('Language'),
        choices=CONSTANTS.LANGUAGE_CHOICES,
        default="",
    )
    # languages = fields.RadioField(
    #     _('Language'),
    #     choices=CONSTANTS.LANGUAGE_CHOICES,
    #     default="",
    # )
    languages_other = fields.TextField(
        _('Please specify other languages'),
        [Optional(), validators.Length(max=64)]
    )
    has_interpreter_yn = fields.SelectField(
        _("Do you have access to an interpreter?"),
        choices=CONSTANTS.YNNA_CHOICES,
        default=""
    )
    education_level = fields.TextField(
        _("What is your highest level of education?"),
        [validators.Length(max=16)]
    )
    marital_status = fields.SelectField(
        _('Marital status'),
        choices=CONSTANTS.MARITAL_STATUS_CHOICES,
        default="",
    )
    veteran_yn = fields.SelectField(
        _('Are you a veteran of the United States?'),
        choices=CONSTANTS.YN_CHOICES,
        default="",
    )
    housing_status = fields.SelectField(
        _('Living situation'),
        choices=CONSTANTS.HOUSING_STATUS_CHOICES,
        default="",
    )
    housing_status_other = fields.TextField(
        _('Please specify other living situation'),
        [Optional(), validators.Length(max=32)]
    )

    # How long have you lived in the greater Richmond area?
    # .time_living_in_area is parent node
    # years_living_in_area = fields.IntegerField(_("Years"), [Optional()])
    # months_living_in_area = fields.IntegerField(_("Months"), [Optional()])
    time_in_area = fields.SelectField(
        _('How long have you lived in the Greater Richmond area?'),
        choices=CONSTANTS.TIME_IN_AREA,
        default=""
    )
    city_or_county_of_residence = fields.TextField(
        _('City or County of Residence'),
        [validators.Length(max=64)]
    )
    temp_visa_yn = fields.SelectField(
        _("Are you traveling in the U.S. on a temporary Visa?"),
        choices=CONSTANTS.YN_CHOICES,
        default="",
    )

    # has_transport_yn = db.Column(db.String(1), info='Has transportation?')

    # EMPLOYMENT
    # student_status = db.Column(db.String(16), info='Are you currently a student?')
    student_status = fields.SelectField(
        _('Student status'),
        choices=CONSTANTS.STUDENT_STATUS_CHOICES,
        default="",
    )
    employment_status = fields.SelectField(
        _('Employment status'),
        choices=CONSTANTS.EMPLOYMENT_STATUS_CHOICES,
        default="",
    )
    spouse_employment_status = fields.SelectField(
        _('Spouse\'s employment status'),
        choices=CONSTANTS.EMPLOYMENT_STATUS_CHOICES,
        default="",
    )

    # How long have you been unemployed?
    # time_unemployed is the parent node
    years_unemployed = fields.IntegerField(_("Years"), [Optional()])
    months_unemployed = fields.IntegerField(_("Months"), [Optional()])
    # spouse_time_unemployed is the parent node
    spouse_years_unemployed = fields.IntegerField(_("Years"), [Optional()])
    spouse_months_unemployed = fields.IntegerField(_("Months"), [Optional()])
    # employment_changes
    # spouse_employment_changes
    employers = fields.FieldList(fields.FormField(
        EmployerForm
    ))
    years_at_current_employer = fields.SelectField(
        _('Years at current employer'),
        choices=CONSTANTS.TIME_AT_CURRENT_EMPLOYER,
        default=""
    )
    spouse_years_at_current_employer = fields.SelectField(
        _('Spouse\'s years at current employer'),
        choices=CONSTANTS.TIME_AT_CURRENT_EMPLOYER,
        default=""
    )
    
    

    # HEALTHCARE/COVERAGE
    last_healthcare = fields.TextField(
        _('When and where did you last receive healthcare services?'),
        [Optional(), validators.Length(max=128)]
    )
    insurance_status = fields.SelectField(
        _('Do you have insurance or a card to help you cover medical costs?'),
        choices=CONSTANTS.YN_CHOICES,
        default="",
    )
    coverage_type = fields.SelectField(
        _('Coverage type'),
        choices=CONSTANTS.COVERAGE_TYPE_CHOICES,
        default="",
    )
    coverage_type_other = fields.TextField(
        _('Please specify other coverage type'),
        [Optional(), validators.Length(max=32)]
    )
    has_prescription_coverage_yn = fields.SelectField(
        _('Do you have prescription drug coverage?'),
        choices=CONSTANTS.YNN_CHOICES,
        default=""
    )
    has_vcc = fields.SelectField(
        _("Do you have a VCC Card?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    # has_pcp_yn
    # has_psychiatrist_yn
    # wants_psychiatrist_yn
    eligible_insurance_types = fields.SelectField(
        _('Are you eligible for insurance coverage through one of the following?'),
        choices=CONSTANTS.COVERAGE_ELIGIBILITY_CHOICES,
        default=""
    )
    applied_for_vets_benefits_yn = fields.SelectField(
        _("Have you applied for veteran's benefits?"),
        choices=CONSTANTS.YNNA_CHOICES,
        default=""
    )
    eligible_for_vets_benefits_yn = fields.SelectField(
        _("Are you eligible for veteran's benefits?"),
        choices=CONSTANTS.YNN_CHOICES,
        default=""
    )
    applied_for_medicaid_yn = fields.SelectField(
        _("Have you ever applied for Medicaid?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    medicaid_date_effective = fields.DateField(
        _("Medicaid date effective"),
        [Optional()]
    )
    applied_for_ssd_yn = fields.SelectField(
        _("Have you ever applied for Social Security Disability?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    ssd_date_effective = fields.DateField(
        _("SSD date effective"),
        [Optional()],
    )
    care_due_to_accident_yn = fields.SelectField(
        _("Is your healthcare the result of an accident?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    accident_work_related_yn = fields.SelectField(
        _("Was the accident work-related?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    # recently_lost_insurance_yn = fields.SelectField(
    #     _("Have you lost your health benefits within the past year?"),
    #     choices = CONSTANTS.YN_CHOICES,
    #     default = ""
    # )

    # INCOME/FINANCES
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
    filed_taxes_yn = fields.SelectField(
        _("Did you file taxes in the last year?"),
        choices=CONSTANTS.YN_CHOICES,
        default=""
    )
    claimed_as_dependent_yn = fields.SelectField(
        _("Did someone else claim you on their return?"),
        choices=CONSTANTS.YNN_CHOICES,
        default=""
    )
    how_food_and_shelter = fields.TextField(
        _('How do you provide food and shelter for yourself or your family?'),
        [Optional(), validators.Length(max=128)]
    )
    how_other_expenses = fields.TextField(
        _('How do you provide for other daily living expenses, \
            such as bills or medications, for yourself or your family?'),
        [Optional(), validators.Length(max=128)]
    )
