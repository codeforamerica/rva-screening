import datetime, time, os, base64, hmac, urllib
from flask import (
  Blueprint,
  render_template,
  request,
  redirect,
  url_for,
  g,
  send_from_directory,
  session,
  current_app,
  jsonify
)
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import db, bcrypt, login_manager
from app.forms import PatientForm, PrescreenForm, ScreeningResultForm
from app.models import *
from app.utils import upload_file, send_document_image
from hashlib import sha1
from itertools import chain
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import subqueryload

screener = Blueprint('screener', __name__, url_prefix='')

@screener.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    user = AppUser.query.filter(AppUser.email == request.form['email']).first()
    if user:
      if bcrypt.check_password_hash(user.password.encode('utf8'), request.form['password']):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('screener.index'))
      else:
        return redirect(url_for('screener.login'))
    else:
      return redirect(url_for('screener.login'))
  else:
    return render_template("login.html")

@screener.route("/logout", methods=["GET"])
@login_required
def logout():
  user = current_user
  user.authenticated = False
  db.session.add(user)
  db.session.commit()
  logout_user()
  return redirect(url_for('screener.login'))

@login_manager.user_loader
def load_user(email):
  return AppUser.query.filter(AppUser.email == email).first()

@screener.before_request
def before_request():
  g.user = current_user

@screener.route('/new_patient' , methods=['POST', 'GET'])
@login_required
def new_patient():
  form = PatientForm()

  if form.validate_on_submit():
    patient = Patient()
    update_patient(patient, form, request.files)
    service = Service.query.get(current_user.service_id)
    patient.services.append(service)
    db.session.add(patient)
    db.session.commit()
    return redirect(url_for('screener.patient_details', id=patient.id))
  else:
    # Check whether we already have some data from a pre-screening
    # if 'household_size' in session or 'household_income' in session:
    #   patient = Patient(
    #     household_size = session.get('household_size'),
    #     household_income = session.get('household_income')
    #   )
    #   session.clear()
    #   return render_template('patient_details.html', patient=patient)
    return render_template('patient_details.html', patient={}, form=form)

@screener.route('/patient_details/<id>', methods=['POST', 'GET'])
@login_required
def patient_details(id):
  patient = Patient.query.get(id)
  form = PatientForm(obj=patient)

  if request.method == 'POST' and form.validate_on_submit():
    update_patient(patient, form, request.files)
    db.session.commit()
    return redirect(url_for('screener.patient_details', id=patient.id))
  else:
    if request.method == 'GET':
      # If the user's service doesn't have permission to see this patient yet,
      # redirect to consent page
      #if current_user.service_id not in [service.id for service in patient.services]:
      #  return redirect(url_for('screener.consent', patient_id = patient.id))

      # If this patient has a referral to the current organization in SENT status,
      # update it to RECEIVED
      referrals = PatientReferral.query.filter(and_(
        PatientReferral.patient_id == patient.id,
        PatientReferral.to_service_id == current_user.service.id
      ))
      sent_referrals = [
        r for r in patient.referrals
        if r.to_service_id == current_user.service_id
        and r.in_sent_status()
      ]
      for referral in sent_referrals:
        referral.mark_received()
      if sent_referrals:
        db.session.commit()

      patient.total_annual_income = sum(
        source.monthly_amount * 12 for source in patient.income_sources if source.monthly_amount
      )
      patient.fpl_percentage = calculate_fpl(
        patient.household_members.count() + 1,
        patient.total_annual_income
      )
    return render_template('patient_details.html', patient=patient, form=form)

def update_patient(patient, form, files):
  for field_name, class_name in [
    ('income_sources', IncomeSource),
    ('phone_numbers', PhoneNumber),
    ('addresses', Address),
    ('emergency_contacts', EmergencyContact),
    ('household_members', HouseholdMember),
    ('employers', Employer)
  ]:
    if form[field_name]:
      # If the last row from the form doesn't have any data, don't save it
      if not bool([val for key, val in form[field_name][-1].data.iteritems() if (
        val != ''
        and val is not None
        and key != 'id'
        and not (key == 'state' and val == 'VA')
      )]):
        form[field_name].pop_entry()

      new_row_count = len(form[field_name].entries) - getattr(patient, field_name).count()
      if new_row_count > 0:
        for p in range(new_row_count):
          getattr(patient, field_name).append(class_name())

      # If any existing rows have no data, delete them from patient object
      for row in form[field_name]:
        if not bool([val for key, val in row.data.iteritems() if (
          val != ''
          and val is not None
          and key != 'id'
          and not (key == 'state' and val == 'VA')
        )]):
          index = int(row.name[-1])
          # Delete from patient object
          db.session.delete(getattr(patient, field_name)[index])
          # Deletion from form FieldList requires popping all entries
          # after the one to be removed, then readding them
          to_re_add = []
          for _ in range(len(form[field_name].entries) - index):
            to_re_add.append(form[field_name].pop_entry())
          to_re_add.pop()
          for row in to_re_add:
            form[field_name].append_entry(data=row.data)

  # populate_obj won't work for file uploads; save them manually
  for entry in form.document_images:
    if entry['id'].data != None:
      document_image = DocumentImage.query.get(entry['id'].data)
      document_image.file_description = entry.file_description.data
    else:
      for _file in files.values():
        filename = upload_file(_file)
        document_image = DocumentImage(
          file_description = entry.file_description.data,
          file_name = filename
        )
        patient.document_images.append(document_image)
        db.session.add(document_image)
        break
  del form.document_images

  form.populate_obj(patient)

  return

def calculate_fpl(household_size, annual_income):
  fpl = 5200 * int(household_size) + 9520
  return float(annual_income) / fpl * 100

@screener.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete(id):
  patient = Patient.query.get(id)
  db.session.delete(patient)
  db.session.commit()
  return redirect(url_for('screener.index'))

@screener.route('/document_image/<image_id>')
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

@screener.route('/documentimages/<filename>')
@login_required
def get_image(filename):
  return send_document_image(filename)

@screener.route('/new_prescreening/<patient_id>', methods=['POST', 'GET'])
@screener.route('/new_prescreening', defaults={'patient_id': None}, methods=['POST', 'GET'])
@login_required
def new_prescreening(patient_id):
  if request.method == 'POST':
    session['service_ids'] = request.form.getlist('services')
    return redirect(url_for('screener.prescreening_basic'))
  if patient_id is not None:
    session.clear()
    session['patient_id'] = patient_id
  services = Service.query.all()
  return render_template('new_prescreening.html', services=services)

@screener.route('/prescreening_basic', methods=['POST', 'GET'])
@login_required
def prescreening_basic():
  form = PrescreenForm()
  if form.validate_on_submit():
    session['household_size'] = form.household_size.data
    session['household_income'] = form.household_income.data
    session['has_health_insurance'] = form.has_health_insurance.data
    session['is_eligible_for_medicaid'] = form.eligible_for_medicaid.data
    return redirect(url_for('screener.prescreening_results'))
  else:
    if session.get('patient_id'):
      patient = Patient.query.get(session['patient_id'])
      return render_template('prescreening_basic.html', patient = patient, form=form)
    else:
      return render_template('prescreening_basic.html', form=form)

def calculate_pre_screen_results(fpl):
  service_results = []
  for service_id in session['service_ids']:
    service = Service.query.get(service_id)

    if (service.fpl_cutoff and fpl > service.fpl_cutoff):
      eligible = False
      fpl_eligible = False
    elif ((service.uninsured_only_yn == 'Y' and session['has_health_insurance'] == 'yes') or
      (service.medicaid_ineligible_only_yn == 'Y' and session['is_eligible_for_medicaid'] == 'yes')):
      eligible = False
      fpl_eligible = True
    else:
      eligible = True
      fpl_eligible = True

    sliding_scale_name = None
    sliding_scale_range = None
    sliding_scale_fees = None
    for sliding_scale in service.sliding_scales:
      if ((sliding_scale.fpl_low <= fpl < sliding_scale.fpl_high)
        or (sliding_scale.fpl_low <= fpl and sliding_scale.fpl_high is None)):
        sliding_scale_name = sliding_scale.scale_name
        sliding_scale_fees = sliding_scale.sliding_scale_fees
        if sliding_scale.fpl_high:
          sliding_scale_range = 'between %d%% and %d%%' % (sliding_scale.fpl_low, sliding_scale.fpl_high)
        else:
          sliding_scale_range = 'over %d%%' % sliding_scale.fpl_low

    service_results.append({
      'name': service.name,
      'eligible': eligible,
      'fpl_cutoff': service.fpl_cutoff,
      'fpl_eligible': fpl_eligible,
      'uninsured_only_yn': service.uninsured_only_yn,
      'medicaid_ineligible_only_yn': service.medicaid_ineligible_only_yn,
      'residence_requirement_yn': service.residence_requirement_yn,
      'time_in_area_requirement_yn': service.time_in_area_requirement_yn,
      'sliding_scale': sliding_scale_name,
      'sliding_scale_range': sliding_scale_range,
      'sliding_scale_fees': sliding_scale_fees,
      'id': service.id
    })

  return service_results

@screener.route('/prescreening_results')
@login_required
def prescreening_results():
  if 'services' in session:
    services = session['services']
  # if 'patient_id' in session and session['patient_id']:
  #   return render_template(
  #     'prescreening_results.html',
  #     services = calculate_pre_screen_results(),
  #     patient_id = session['patient_id']
  #   )
  # else:
  fpl = calculate_fpl(session['household_size'], int(session['household_income']) * 12)
  return render_template(
    'prescreening_results.html',
    services = calculate_pre_screen_results(fpl),
    household_size = session['household_size'],
    household_income = int(session['household_income']) * 12,
    fpl = fpl,
    has_health_insurance = session['has_health_insurance'],
    is_eligible_for_medicaid = session['is_eligible_for_medicaid']
  )

@screener.route('/save_prescreening_updates')
@login_required
def save_prescreening_updates():
  if 'patient_id' in session and session['patient_id']:
    patient_id = session['patient_id']
    patient = Patient.query.get(session['patient_id'])
    patient.household_size = session['household_size']
    patient.household_income = session['household_income']
    db.session.commit()
    session.clear()
    return redirect(url_for('screener.patient_details', id = patient_id))

# SEARCH NEW PATIENT
@screener.route('/search_new' )
@login_required
def search_new():
  patients = Patient.query.all()
  patients = Patient.query.filter(~Patient.services.any(Service.id == current_user.service_id))
  return render_template('search_new.html', patients=patients)

# PRINT PATIENT DETAILS
# @param patient id
@screener.route('/patient_print/<patient_id>')
@login_required
def patient_print(patient_id):
  patient = Patient.query.get(patient_id)
  form = PatientForm(obj=patient)
  return render_template('patient_details.html', patient=patient, form=form)

@screener.route('/consent/<patient_id>')
@login_required
def consent(patient_id):
  patient = Patient.query.get(patient_id)
  return render_template('consent.html', patient=patient)

@screener.route('/consent_given/<patient_id>')
@login_required
def consent_given(patient_id):
  service_permission = PatientServicePermission(
    patient_id = patient_id,
    service_id = current_user.service_id
  )
  db.session.add(service_permission)
  db.session.commit()
  return redirect(url_for('screener.patient_details', id = patient_id))

@screener.route('/add_referral', methods=["POST"])
@login_required
def add_referral():
  referral = PatientReferral(
    patient_id = request.form['patient_id'],
    from_app_user_id = request.form['app_user_id'],
    to_service_id = request.form['service_id'],
    status = 'SENT'
  )
  db.session.add(referral)
  db.session.commit()
  return jsonify()

# TEMPLATE PROTOTYPING
# This is a dev-only route for prototyping fragments of other templates without touching
# them. The url should not be linked anywhere, and ideally it should be not be
# accessible in the deplyed version.
@screener.route('/template_prototyping/')
def template_prototyping():
    return render_template('template_prototyping.html')

@screener.route('/patient_history/<patient_id>')
@login_required
def patient_history(patient_id):
  patient = Patient.query.get(patient_id)

  history = ActionLog.query.\
    filter(or_(
      and_(ActionLog.row_id==patient_id, ActionLog.table_name=='patient'),
      and_(ActionLog.row_id.in_([p.id for p in patient.phone_numbers]), ActionLog.table_name=='phone_number'),
      and_(ActionLog.row_id.in_([p.id for p in patient.addresses]), ActionLog.table_name=='address'),
      and_(ActionLog.row_id.in_([p.id for p in patient.emergency_contacts]), ActionLog.table_name=='emergency_contact'),
      and_(ActionLog.row_id.in_([p.id for p in patient.employers]), ActionLog.table_name=='employer'),
      and_(ActionLog.row_id.in_([p.id for p in patient.document_images]), ActionLog.table_name=='document_image'),
      and_(ActionLog.row_id.in_([p.id for p in patient.income_sources]), ActionLog.table_name=='income_source'),
      and_(ActionLog.row_id.in_([p.id for p in patient.household_members]), ActionLog.table_name=='household_member'),
      and_(ActionLog.row_id.in_([p.id for p in patient.patient_service_permissions]), ActionLog.table_name=='patient_service_permission')
    )).\
    order_by(ActionLog.action_timestamp.desc())
  # Filter out history entries that are only last modified/last modified by changes
  history = [i for i in history if not (
    i.changed_fields
    and set(i.changed_fields).issubset(['last_modified', 'last_modified_by'])
  )]

  services = dict((x.id, x) for x in Service.query.all())

  readable_names = dict(
    (column.name, column.info) for column in
      chain(
        Patient.__table__.columns,
        PhoneNumber.__table__.columns,
        Address.__table__.columns,
        EmergencyContact.__table__.columns,
        HouseholdMember.__table__.columns,
        IncomeSource.__table__.columns,
        Employer.__table__.columns,
        DocumentImage.__table__.columns
      )
  )

  return render_template(
    'history.html',
    patient=patient,
    history=history,
    services=services,
    readable_names=readable_names
  )

# SHARE PATIENT DETAILS
# @param patient id
@screener.route('/patient_share/<patient_id>')
@login_required
def patient_share(patient_id):
  patient = Patient.query.get(patient_id)
  services = Service.query.all()
  return render_template(
    'patient_share.html',
    patient = patient,
    services = services,
    current_user = current_user
  )

# USER PROFILE
@screener.route('/user/<user_id>')
@login_required
def user(user_id):
  print "USER ID"
  print user_id
  user = AppUser.query.get(user_id)
  return render_template('user_profile.html', user=user)

# SERVICE PROFILE
@screener.route('/service/<service_id>')
@login_required
def service(service_id):
  service = translate_object(
    Service.query.get(service_id),
    current_app.config['BABEL_DEFAULT_LOCALE']
  )
  return render_template('service_profile.html', service=service)

def translate_object(obj, language_code):
  translations = next(
    (lang for lang in obj.translations if lang.language_code == language_code),
    None
  ) 
  if translations is not None:
    for key, value in translations.__dict__.iteritems():
      if (
        value is not None 
        and not key.startswith('_')
        and hasattr(obj, key)
      ):
        setattr(obj, key, getattr(translations, key))
  return obj

@screener.route('/patient_screening_history/<patient_id>', methods=['POST', 'GET'])
@login_required
def patient_screening_history(patient_id):
  patient = Patient.query.get(patient_id)
  form = ScreeningResultForm()
  sliding_scale_options = SlidingScale.query.filter(
    SlidingScale.service_id == current_user.service_id
  )
  # Add the current organization's sliding scale options to the dropdown
  form.sliding_scale_id.choices = [
    (option.id, option.scale_name) for option in sliding_scale_options
  ] or [("", "N/A")]

  if form.validate_on_submit():
    screening_result = PatientScreeningResult()
    screening_result.service_id = current_user.service_id
    screening_result.eligible_yn = form.eligible_yn.data
    screening_result.sliding_scale_id = form.sliding_scale_id.data or None
    screening_result.notes = form.notes.data
    patient.screening_results.append(screening_result)

    # If the patient has an open referral to the current organization, mark
    # as completed
    open_referrals = [
      r for r in patient.referrals
      if r.to_service_id == current_user.service.id
      and r.in_received_status()
    ]
    for referral in open_referrals:
      referral.mark_completed()

    db.session.commit()

  return render_template('patient_screening_history.html', patient=patient, form=form)

@screener.route('/')
@login_required
def index():
  session.clear()
  #patients = Patient.query.filter(Patient.services.any(Service.id == current_user.service_id))
  all_patients = Patient.query.all()
  recently_updated = Patient.query.filter(or_(
    Patient.last_modified > datetime.date.today() - datetime.timedelta(days=7),
    Patient.created > datetime.date.today() - datetime.timedelta(days=7)
  ))
  open_referrals = Patient.query.filter(
    Patient.referrals.any(and_(
      PatientReferral.to_service_id == current_user.service_id,
      PatientReferral.status in ['SENT', 'RECEIVED']
    ))
  )
  your_referrals = Patient.query.filter(
    Patient.referrals.any(
      PatientReferral.from_app_user_id == current_user.id
    )
  )

  return render_template(
    'index.html',
    all_patients = all_patients,
    recently_updated = recently_updated,
    open_referrals = open_referrals,
    your_referrals = your_referrals
  )
