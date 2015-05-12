from flask import render_template, request,flash, redirect, url_for, g, send_from_directory, session
from app import app, db, bcrypt, ALLOWED_EXTENSIONS
from app.models import Patient, PhoneNumber, Address, EmergencyContact, Insurance, HouseholdMember, IncomeSource, Employer, DocumentImage, Service, User
import datetime
import os
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import login_manager
from werkzeug import secure_filename

# example data for front-end prototyping
from app import example_data as EXAMPLE_DATA

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
    emergency_contact = EmergencyContact(
      name = form['emergency_contact_name'],
      relationship = form['emergency_contact_relation'],
      phone_number = form['emergency_contact_phone']
    )
    patient.emergency_contacts.append(emergency_contact)

    db.session.add(patient)
    db.session.add(emergency_contact)
    db.session.commit()

    for file in request.files.itervalues():
      if allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)
        document_image = DocumentImage(patient.id, file_name)
        db.session.add(document_image)
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
    phone_numbers = request.form.getlist('phone_number')
    phone_descriptions = request.form.getlist('phone_description')
    phone_primary_yns = request.form.getlist('phone_primary_yn')
    for index, value in enumerate(phone_numbers):
      phone_number = PhoneNumber(
        phone_number=value,
        description = phone_descriptions[index]
      )
      patient.phone_numbers.append(phone_number)
      db.session.add(phone_number)

    address1s = request.form.getlist('address1')
    address2s = request.form.getlist('address2')
    cities = request.form.getlist('city')
    states = request.form.getlist('state')
    zips = request.form.getlist('zip')
    address_descriptions = request.form.getlist('address_description')
    for index, value in enumerate(address1s):
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

    for key, value in request.form.iteritems():
      if key == 'dob' and value != '':
        value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
      if value == '':
        value = None
      setattr(patient, key, value)

    for file in request.files.itervalues():
      if allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)
        document_image = DocumentImage(patient_id=patient.id, file_name=file_name)
        db.session.add(document_image)

    db.session.commit()
    return redirect(url_for('index'))
  else:
    if not patient:
        patient = EXAMPLE_DATA.example_patient
    return render_template('patient_details.html', patient=patient)

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
    return redirect(url_for('prescreening_results'))
  else:
    if session.get('patient_id'):
      patient = Patient.query.get(session['patient_id'])
      return render_template('prescreening_basic.html', patient = patient)
    else:
      return render_template('prescreening_basic.html')

@app.route('/prescreening_results')
@login_required
def prescreening_results():
  if 'services' in session:
    services = session['services']
  else:
    services = EXAMPLE_DATA.services
  if 'patient_id' in session and session['patient_id']:
    return render_template(
      'prescreening_results.html',
      services = services,
      patient_id = session['patient_id']
    )
  else:
    return render_template('prescreening_results.html', services = services)

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

@app.route('/search_new' )
@login_required
def search_new():
  patients = Patient.query.all()
  return render_template('search.html', patients=patients)

@app.route('/' )
@login_required
def index():
  session.clear()
  patients = Patient.query.all()
  if not patients:
      patients = EXAMPLE_DATA.patients
  return render_template('index.html', patients=patients)
