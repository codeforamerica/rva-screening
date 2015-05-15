from flask import render_template, request,flash, redirect, url_for, g, send_from_directory, session
from app import app, db, bcrypt, ALLOWED_EXTENSIONS
from app.models import Patient, PhoneNumber, Address, EmergencyContact, Insurance, HouseholdMember, IncomeSource, Employer, DocumentImage, Service, User
import datetime
import os
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import login_manager
from werkzeug import secure_filename
from sqlalchemy import func

DAILY_PLANET_FEES = {
  'Nominal': (
    ('Dental services', 30),
    ('Medical services', 10),
    ('Mental health services, initial visit of calendar month', 10),
    ('Mental health services, other visits', 5)
  ),
  'Slide A': (
    ('Dental services', '45\% of full fee'),
    ('Medical services', 15),
    ('Mental health services, initial visit of calendar month', 15),
    ('Mental health services, second visit of calendar month', 10),
    ('Mental health services, other visits', 5)
  ),
  'Slide B': (
    ('Dental services', '55\% of full fee'),
    ('Medical services', 20),
    ('Mental health services, initial visit of calendar month', 20),
    ('Mental health services, second visit of calendar month', 15),
    ('Mental health services, other visits', 5)
  ),
  'Slide C': (
    ('Dental services', '65\% of full fee'),
    ('Medical services', 30),
    ('Mental health services, initial visit of calendar month', 30),
    ('Mental health services, second visit of calendar month', 25),
    ('Mental health services, other visits', 5)
  ),
  'Full fee': ()
}
CROSSOVER_FEES = (
  ('Medications', 4),
  ('Nurse/Labs', 10),
  ('Vaccine clinic', 10),
  ('Medical visit/mental health', 15),
  ('Eye', 15),
  ('Same day appointments', 20),
  ('Dental', 25)
)

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    user = User.query.filter(User.email == request.form['email']).first()
    if user:
      if bcrypt.check_password_hash(user.password.encode('utf8'), request.form['password']):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
  else:
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  user = current_user
  user.authenticated = False
  db.session.add(user)
  db.session.commit()
  logout_user()
  return redirect(url_for('index'))

@login_manager.user_loader
def load_user(email):
  return User.query.filter(User.email == email).first()

@app.before_request
def before_request():
  g.user = current_user

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/new_patient' , methods=['POST', 'GET'])
@login_required
def new_patient():
  if request.method == 'POST':

    form = dict((key, value) for key, value in request.form.iteritems())
    if form.get('dob'):
      form['dob'] = datetime.datetime.strptime(form['dob'], '%Y-%m-%d').date()
    for key, value in form.iteritems():
      if value == '':
        form[key] = None
    patient = Patient(**form)

    db.session.add(patient)
    many_to_one_patient_updates(patient, request.form, request.files)
    db.session.commit()

    return redirect(url_for('index'))
  else:
    # Check whether we already have some data from a pre-screening
    if 'household_size' in session or 'household_income' in session:
      patient = Patient(
        household_size = session.get('household_size'),
        household_income = session.get('household_income')
      )
      session.clear()
      return render_template('patient_details.html', patient=patient)

    return render_template('patient_details.html', patient={})

@app.route('/patient_details/<id>', methods=['POST', 'GET'])
@login_required
def patient_details(id):
  patient = Patient.query.get(id)

  if request.method == 'POST':
    many_to_one_patient_updates(patient, request.form, request.files)

    for key, value in request.form.iteritems():
      if key == 'dob' and value != '':
        value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
      if value == '':
        value = None
      setattr(patient, key, value)

    db.session.commit()
    return redirect(url_for('index'))
  else:
    patient.total_annual_income = sum(
      source.annual_amount for source in patient.income_sources
    )
    patient.fpl_percentage = calculate_fpl(
      patient.household_members.count() + 1,
      patient.total_annual_income
    )
    return render_template('patient_details.html', patient=patient)

def many_to_one_patient_updates(patient, form, files):
  phone_number_ids = form.getlist('phone_number_id')
  phone_numbers = form.getlist('phone_number')
  phone_descriptions = form.getlist('phone_description')
  phone_primary_yns = form.getlist('phone_primary_yn')
  for index, value in enumerate(phone_numbers):
    if value:
      if len(phone_number_ids) > index:
        phone_number = PhoneNumber.query.get(phone_number_ids[index])
        phone_number.phone_number = value
        phone_number.description = phone_descriptions[index]
      else:
        phone_number = PhoneNumber(
          phone_number=value,
          description = phone_descriptions[index]
        )
        patient.phone_numbers.append(phone_number)
        db.session.add(phone_number)

  address_ids = form.getlist('address_id')
  address1s = form.getlist('address1')
  address2s = form.getlist('address2')
  cities = form.getlist('city')
  states = form.getlist('state')
  zips = form.getlist('zip')
  address_descriptions = form.getlist('address_description')
  for index, value in enumerate(address1s):
    if value:
      if len(address_ids) > index:
        address = Address.query.get(address_ids[index])
        address.address1 = value
        address.address2 = address2s[index]
        address.city = cities[index]
        address.state = states[index]
        address.zip = zips[index]
        address.description = address_descriptions[index]
      else:
        address = Address(
          address1 = value,
          address2 = address2s[index],
          city = cities[index],
          state = states[index],
          zip = zips[index],
          description = address_descriptions[index]
        )
        patient.addresses.append(address)
        db.session.add(address)

  household_member_ids = form.getlist('household_member_id')
  household_member_full_names = form.getlist('household_member_full_name')
  household_member_dobs = form.getlist('household_member_dob')
  household_member_ssns = form.getlist('household_member_ssn')
  household_member_relations = form.getlist('household_member_relation')
  for index, value in enumerate(household_member_full_names):
    if value:
      if len(household_member_ids) > index:
        household_member = HouseholdMember.query.get(household_member_ids[index])
        household_member.full_name = value
        household_member.dob = household_member_dobs[index]
        household_member.ssn = household_member_ssns[index]
        household_member.relationship = household_member_relations[index]
      else:
        household_member = HouseholdMember(
          full_name = value,
          dob = household_member_dobs[index],
          ssn = household_member_ssns[index],
          relationship = household_member_relations[index]
        )
        patient.household_members.append(household_member)
        db.session.add(household_member)

  income_source_ids = form.getlist('income_source_id')
  income_sources = form.getlist('income_source_source')
  income_source_amounts = form.getlist('income_source_amount')
  for index, value in enumerate(income_sources):
    if value:
      if len(income_source_ids) > index:
        income_source = IncomeSource.query.get(income_source_ids[index])
        income_source.source = income_sources[index]
        income_source.annual_amount = int(income_source_amounts[index]) * 12
      else:
        income_source = IncomeSource(
          source = value,
          annual_amount = int(income_source_amounts[index]) * 12
        )
        patient.income_sources.append(income_source)
        db.session.add(income_source)

  emergency_contact_ids = form.getlist('emergency_contact_id')
  emergency_contact_names = form.getlist('emergency_contact_name')
  emergency_contact_phone_numbers = form.getlist('emergency_contact_phone_number')
  emergency_contact_relationships = form.getlist('emergency_contact_relationship')
  for index, value in enumerate(emergency_contact_names):
    if value:
      if len(emergency_contact_ids) > index:
        emergency_contact = EmergencyContact.query.get(emergency_contact_ids[index])
        emergency_contact.name = emergency_contact_names[index]
        emergency_contact.phone_number = emergency_contact_phone_numbers[index]
        emergency_contact.relationship = emergency_contact_relationships[index]
      else:
        emergency_contact = EmergencyContact(
          name = value,
          phone_number = emergency_contact_phone_numbers[index],
          relationship = emergency_contact_relationships[index]
        )
        patient.emergency_contacts.append(emergency_contact)
        db.session.add(emergency_contact)

  employer_ids = form.getlist('employer_id')
  employer_employees = form.getlist('employer_employee')
  employer_names = form.getlist('employer_name')
  employer_phone_numbers = form.getlist('employer_phone_number')
  employer_start_dates = form.getlist('employer_start_date')
  for index, value in enumerate(employer_employees):
    if value:
      if len(employer_ids) > index:
        employer = Employer.query.get(employer_ids[index])
        employer.employee = employer_employees[index]
        employer.name = employer_names[index]
        employer.phone_number = employer_phone_numbers[index]
        employer.start_date = employer_start_dates[index]
      else:
        employer = Employer(
          employee = value,
          name = employer_names[index],
          phone_number = employer_phone_numbers[index],
          start_date = employer_start_dates[index]
        )
        patient.employers.append(employer)
        db.session.add(employer)

  document_image_ids = form.getlist('document_image_id')
  document_image_descriptions = form.getlist('document_image_description')
  for index, value in enumerate(document_image_descriptions):
    if value:
      if len(document_image_ids) > index:
        document_image = DocumentImage.query.get(document_image_ids[index])
        document_image.description = document_image_descriptions[index]
      else:
        for file in files.itervalues():
          if allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)
            document_image = DocumentImage(
              patient_id=patient.id,
              file_name=file_name,
              description = document_image_descriptions[index]
            )
            db.session.add(document_image)
            index += 1
        break

  return

def calculate_fpl(household_size, annual_income):
  fpl = 5200 * int(household_size) + 9520
  return float(annual_income) / fpl * 100

@app.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete(id):
  patient = Patient.query.get(id)
  db.session.delete(patient)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/document_image/<image_id>')
@login_required
def document_image(image_id):
  _image = DocumentImage.query.get(image_id)
  file_path = '/documentimages/' + _image.file_name
  return render_template('documentimage.html', file_path=file_path)

@app.route('/documentimages/<filename>')
@login_required
def get_image(filename):
  return send_from_directory(os.path.join(
    app.config['PROJECT_ROOT'],
    app.config['UPLOAD_FOLDER']),
    filename
  )

@app.route('/new_prescreening/<patient_id>', methods=['POST', 'GET'])
@app.route('/new_prescreening', defaults={'patient_id': None}, methods=['POST', 'GET'])
@login_required
def new_prescreening(patient_id):
  if request.method == 'POST':
    session['services'] = request.form.getlist('services')
    return redirect(url_for('prescreening_basic'))
  if patient_id is not None:
    session.clear()
    session['patient_id'] = patient_id
  return render_template('new_prescreening.html')

@app.route('/prescreening_basic', methods=['POST', 'GET'])
@login_required
def prescreening_basic():
  if request.method == 'POST':
    session['household_size'] = request.form['household_size']
    session['household_income'] = request.form['household_income']
    session['has_health_insurance'] = request.form['has_health_insurance']
    session['is_eligible_for_medicaid'] = request.form['is_eligible_for_medicaid']
    return redirect(url_for('prescreening_results'))
  else:
    if session.get('patient_id'):
      patient = Patient.query.get(session['patient_id'])
      return render_template('prescreening_basic.html', patient = patient)
    else:
      return render_template('prescreening_basic.html')

def calculate_pre_screen_results():
  fpl = calculate_fpl(session['household_size'], int(session['household_income']) * 12)
  service_results = []
  for service in session['services']:
    if service == 'daily_planet':
      sliding_scale = daily_planet_pre_screen(fpl)
      service_results.append({
        'name': 'Daily Planet',
        'eligible': True,
        'sliding_scale': sliding_scale,
        'sliding_scale_fees': DAILY_PLANET_FEES[sliding_scale]
      })
    if service == 'resource_centers':
      service_results.append({
        'name': 'RCHD resource centers',
        'eligible': True,
        'sliding_scale': resource_center_pre_screen(fpl)
      })
    if service == 'cross_over':
      service_results.append({
        'name': 'CrossOver',
        'eligible': cross_over_pre_screen(
          fpl,
          session['has_health_insurance'],
          session['is_eligible_for_medicaid']
        ),
        'sliding_scale': 0,
        'general_fees': CROSSOVER_FEES
      })
    if service == 'access_now':
      service_results.append({
        'name': 'Access Now',
        'eligible': access_now_pre_screen(
          fpl,
          session['has_health_insurance'],
          session['is_eligible_for_medicaid']
        ),
        'sliding_scale': 0
      })
  return service_results

def daily_planet_pre_screen(fpl):
  if fpl <= 100:
    sliding_scale = 'Nominal'
  elif 100 < fpl <= 125:
    sliding_scale = 'A'
  elif 125 < fpl <= 150:
    sliding_scale = 'B'
  elif 150 <fpl <= 200:
    sliding_scale = 'C'
  else:
    sliding_scale = 'Full fee'
  return sliding_scale

def resource_center_pre_screen(fpl):
  if fpl <= 100:
    sliding_scale = 'Nominal'
  elif 100 < fpl <= 125:
    sliding_scale = 'A'
  elif 125 < fpl <= 150:
    sliding_scale = 'B'
  elif 150 <fpl <= 200:
    sliding_scale = 'C'
  else:
    sliding_scale = 'Full fee'
  return sliding_scale

def cross_over_pre_screen(fpl, has_health_insurance, is_eligible_for_medicaid):
  print fpl
  print has_health_insurance
  print is_eligible_for_medicaid
  if fpl <= 200 and has_health_insurance == 'no' and is_eligible_for_medicaid == 'no':
    return True
  else:
    return False

def access_now_pre_screen(fpl, has_health_insurance, is_eligible_for_medicaid):
  if fpl <= 200 and has_health_insurance == 'no' and is_eligible_for_medicaid == 'no':
    return True
  else:
    return False

@app.route('/prescreening_results')
@login_required
def prescreening_results():
  if 'services' in session:
    services = session['services']
  if 'patient_id' in session and session['patient_id']:
    return render_template(
      'prescreening_results.html',
      services = services,
      patient_id = session['patient_id']
    )
  else:
    return render_template(
      'prescreening_results.html',
      services = calculate_pre_screen_results()
    )

@app.route('/save_prescreening_updates')
@login_required
def save_prescreening_updates():
  if 'patient_id' in session and session['patient_id']:
    patient_id = session['patient_id']
    patient = Patient.query.get(session['patient_id'])
    patient.household_size = session['household_size']
    patient.household_income = session['household_income']
    db.session.commit()
    session.clear()
    return redirect(url_for('patient_details', id = patient_id))

# SEARCH NEW PATIENT
@app.route('/search_new' )
@login_required
def search_new():
  patients = Patient.query.all()
  return render_template('search_new.html', patients=patients)

# PRINT PATIENT DETAILS
# @param patient id
@app.route('/patient_print/<patient_id>')
@login_required
def patient_print(patient_id):
  patient = Patient.query.get(patient_id)
  return render_template('print.html', patient=patient)

@app.route('/patient_history/<patient_id>')
@login_required
def patient_history(patient_id):
  patient = Patient.query.get(patient_id)
  return render_template('history.html', patient=patient, request=request)

# SHARE PATIENT DETAILS
# @param patient id
@app.route('/patient_share/<patient_id>')
@login_required
def patient_share(patient_id):
  patient = Patient.query.get(patient_id)
  return render_template('patient_share.html', patient=patient)

@app.route('/' )
@login_required
def index():
  session.clear()
  patients = Patient.query.all()
  return render_template('index.html', patients=patients)
