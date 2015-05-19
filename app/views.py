import time, os, base64, hmac, urllib
from flask import render_template, request,flash, redirect, url_for, g, send_from_directory, session, current_app
from app import app, db, bcrypt
from app.models import Patient, PhoneNumber, Address, EmergencyContact, Insurance, HouseholdMember, IncomeSource, Employer, DocumentImage, Service, User
import datetime
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import login_manager
from app.utils import upload_file, send_document_image
from sqlalchemy import func
from hashlib import sha1

DAILY_PLANET_FEES = {
  'Nominal': (
    ('Dental services', 30),
    ('Medical services', 10),
    ('Mental health services, initial visit of calendar month', 10),
    ('Mental health services, other visits', 5)
  ),
  'Slide A': (
    ('Dental services', '45% of full fee'),
    ('Medical services', 15),
    ('Mental health services, initial visit of calendar month', 15),
    ('Mental health services, second visit of calendar month', 10),
    ('Mental health services, other visits', 5)
  ),
  'Slide B': (
    ('Dental services', '55% of full fee'),
    ('Medical services', 20),
    ('Mental health services, initial visit of calendar month', 20),
    ('Mental health services, second visit of calendar month', 15),
    ('Mental health services, other visits', 5)
  ),
  'Slide C': (
    ('Dental services', '65% of full fee'),
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

    return redirect(url_for('patient_details', id=patient.id))
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
    return redirect(url_for('patient_details', id=patient.id))
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
  # Phone numbers
  phone_number_rows = [
    {'id': id, 'phone_number': phone_number, 'description': description, 'primary_yn': primary_yn}
    for id, phone_number, description, primary_yn
    in map(
      None,
      form.getlist('phone_number_id'),
      form.getlist('phone_number'),
      form.getlist('phone_description'),
      form.getlist('phone_primary_yn')
    )
  ]
  for row in phone_number_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and val is not None and key != 'id']):     
      if row['id'] != None:
        phone_number = PhoneNumber.query.get(row['id'])
        phone_number.phone_number = row['phone_number']
        phone_number.description = row['description']
        phone_number.primary_yn = row['primary_yn']
      else:
        phone_number = PhoneNumber(
          phone_number = row['phone_number'],
          description = row['description'],
          primary_yn = row['primary_yn'],
        )
        patient.phone_numbers.append(phone_number)
        db.session.add(phone_number)
    elif row['id'] != None:
      db.session.delete(PhoneNumber.query.get(row['id']))

  # Addresses
  address_rows = [
    {'id': id, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zip_code': zip_code, 'description': description}
    for id, address1, address2, city, state, zip_code, description
    in map(
      None,
      form.getlist('address_id'),
      form.getlist('address1'),
      form.getlist('address1'),
      form.getlist('city'),
      form.getlist('state'),
      form.getlist('zip'),
      form.getlist('address_description'),
    )
  ]
  for row in address_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and key != 'id']):     
      if row['id'] != None:
        address = Address.query.get(row['id'])
        address.address1 = row['address1']
        address.address2 = row['address2']
        address.city = row['city']
        address.state = row['state']
        address.zip = row['zip_code']
        address.description = row['description']
      else:
        address = Address(
          address1 = row['address1'],
          address2 = row['address2'],
          city = row['city'],
          state = row['state'],
          zip = row['zip_code'],
          description = row['description'],
        )
        patient.addresses.append(address)
        db.session.add(address)
    elif row['id'] != None:
      db.session.delete(Address.query.get(row['id']))

  # Household members
  household_member_rows = [
    {'id': id, 'full_name': full_name, 'dob': dob, 'ssn': ssn, 'relation': relation}
    for id, full_name, dob, ssn, relation
    in map(
      None,
      form.getlist('household_member_id'),
      form.getlist('household_member_full_name'),
      form.getlist('household_member_dob'),
      form.getlist('household_member_ssn'),
      form.getlist('household_member_relation'),
    )
  ]
  for row in household_member_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and key != 'id']):     
      if row['id'] != None:
        household_member = HouseholdMember.query.get(row['id'])
        household_member.full_name = row['full_name']
        if row['dob']:
          household_member.dob = row['dob']
        household_member.ssn= row['ssn']
        household_member.relationship = row['relation']
      else:
        household_member = HouseholdMember(
          full_name = row['full_name'],
          dob = row['dob'] or None,
          ssn = row['ssn'],
          relationship = row['relation']
        )
        patient.household_members.append(household_member)
        db.session.add(household_member)
    elif row['id'] != None:
      db.session.delete(HouseholdMember.query.get(row['id']))

  # Income sources
  income_source_rows = [
    {'id': id, 'source': source, 'amount': amount}
    for id, source, amount
    in map(
      None,
      form.getlist('income_source_id'),
      form.getlist('income_source_source'),
      form.getlist('income_source_amount'),
    )
  ]
  for row in income_source_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and key != 'id']):     
      if row['id'] != None:
        income_source = IncomeSource.query.get(row['id'])
        income_source.source = row['source']
        income_source.annual_amount = int(row['amount'] or '0') * 12
      else:
        income_source = IncomeSource(
          source = row['source'],
          annual_amount = int(row['amount'] or '0') * 12
        )
        patient.income_sources.append(income_source)
        db.session.add(income_source)
    elif row['id'] != None:
      db.session.delete(IncomeSource.query.get(row['id']))

  # Emergency contacts
  emergency_contact_rows = [
    {'id': id, 'name': name, 'phone_number': phone_number, 'relationship': relationship}
    for id, name, phone_number, relationship
    in map(
      None,
      form.getlist('emergency_contact_id'),
      form.getlist('emergency_contact_name'),
      form.getlist('emergency_contact_phone_number'),
      form.getlist('emergency_contact_relationship')
    )
  ]
  for row in emergency_contact_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and key != 'id']):     
      if row['id'] != None:
        emergency_contact = EmergencyContact.query.get(row['id'])
        emergency_contact.name = row['name']
        emergency_contact.phone_number = row['phone_number']
        emergency_contact.relationship = row['relationship']
      else:
        emergency_contact = EmergencyContact(
          name = row['name'],
          phone_number = row['phone_number'],
          relationship = row['relationship']
        )
        patient.emergency_contacts.append(emergency_contact)
        db.session.add(emergency_contact)
    elif row['id'] != None:
      db.session.delete(EmergencyContact.query.get(row['id']))

  # Employers
  employer_rows = [
    {'id': id, 'employee': employee, 'name': name, 'phone_number': phone_number, 'start_date': start_date}
    for id, employee, name, phone_number, start_date
    in map(
      None,
      form.getlist('employer_id'),
      form.getlist('employer_employee'),
      form.getlist('employer_name'),
      form.getlist('employer_phone_number'),
      form.getlist('employer_start_date')
    )
  ]
  for row in employer_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and val is not None and key != 'id' and key != 'employee']):     
      if row['id'] != None:
        employer = Employer.query.get(row['id'])
        employer.employee = row['employee']
        employer.name = row['name']
        employer.phone_number = row['phone_number']
        employer.start_date = row['start_date']
      else:
        employer = Employer(
          employee = row['employee'],
          name = row['name'],
          phone_number = row['phone_number'],
          start_date = row['start_date']
        )
        patient.employers.append(employer)
        db.session.add(employer)
    elif row['id'] != None:
      db.session.delete(Employer.query.get(row['id']))

  # Document Images
  document_image_rows = [
    {'id': id, 'description': description}
    for id, description
    in map(
      None,
      form.getlist('document_image_id'),
      form.getlist('document_image_description')
    )
  ]
  for row in document_image_rows:
    # Check that at least one field in the row has data, otherwise delete it
    if bool([val for key, val in row.iteritems() if val != '' and key != 'id']):     
      if row['id'] != None:
        document_image = DocumentImage.query.get(row['id'])
        document_image.description = row['description']
      else:
        for _file in files.getlist('document_image_file'):
          filename = upload_file(_file)
          document_image = DocumentImage(
            description = row['description'],
            file_name = filename
          )
          patient.document_images.append(document_image)
          db.session.add(document_image)
          break
    elif row['id'] != None:
      db.session.delete(DocumentImage.query.get(row['id']))

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
  if current_app.config['SCREENER_ENVIRONMENT'] == 'prod':
    file_path = 'http://s3.amazonaws.com/{bucket}/{uploaddir}/{filename}'.format(
        bucket=current_app.config['S3_BUCKET_NAME'],
        uploaddir=current_app.config['S3_FILE_UPLOAD_DIR'],
        filename=_image.file_name
    )
  else:
    file_path = '/documentimages/' + _image.file_name
  return render_template('documentimage.html', file_path=file_path)

@app.route('/documentimages/<filename>')
@login_required
def get_image(filename):
  return send_document_image(filename)

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
    sliding_scale = 'Slide A'
  elif 125 < fpl <= 150:
    sliding_scale = 'Slide B'
  elif 150 <fpl <= 200:
    sliding_scale = 'Slide C'
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
      services = calculate_pre_screen_results(),
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
  return render_template('patient_details.html', patient=patient)

# PATIENT DETAILS (NEW)
#
# this is a tempomrary route that shows what viewing a new patient
# will look like. When the page loads, it will have an alert asking
# for consent
#
# TODO: this will essentially be part of the patient_details route
# to check if the user has permission to view the patient. When that
# functionality is added we should delete the patient_details_new.html
# template
@app.route('/consent/')
@login_required
def consent():
  # this is temporary!
  patients = Patient.query.all()
  first = patients[0]
  print first.id
  return render_template('consent.html', patient=first)

@app.route('/patient_history/<patient_id>')
@login_required
def patient_history(patient_id):
  patient = Patient.query.get(patient_id)
  return render_template('history.html', patient=patient)

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
