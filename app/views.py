import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    g,
    session,
    current_app,
    jsonify
)
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import db, bcrypt, login_manager
from app.forms import PatientForm, PrescreenForm, ScreeningResultForm
from app.models import (
    AppUser,
    Patient,
    PhoneNumber,
    Address,
    Employer,
    IncomeSource,
    HouseholdMember,
    DocumentImage,
    EmergencyContact,
    Service,
    ActionLog,
    PatientReferral,
    SlidingScale,
    PatientScreeningResult
)
from app.prescreening import calculate_fpl, calculate_pre_screen_results
from app.utils import upload_file, send_document_image, translate_object
from itertools import chain
from sqlalchemy import and_, or_
from werkzeug.datastructures import FileStorage


screener = Blueprint('screener', __name__, url_prefix='')


@screener.before_request
def before_request():
    g.user = current_user


@screener.route("/login", methods=["GET", "POST"])
def login():
    """Display login page and check credentials."""
    if request.method == 'POST':
        user = AppUser.query.filter(AppUser.email == request.form['email']).first()
        if user:
            if bcrypt.check_password_hash(
                user.password.encode('utf8'),
                request.form['password']
            ):
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
    """Log the user out and redirect to login page."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('screener.login'))


@login_manager.user_loader
def load_user(email):
    """Look up the user by email address."""
    return AppUser.query.filter(AppUser.email == email).first()


@screener.route('/new_patient', methods=['POST', 'GET'])
@login_required
def new_patient():
    """Display the form for a new patient, and create a new patient after submission."""
    form = PatientForm()

    if form.validate_on_submit():
        patient = Patient()
        update_patient(patient, form, request.files)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('screener.patient_details', id=patient.id))
    else:
        return render_template('patient_details.html', patient={}, form=form)


@screener.route('/patient_details/<id>', methods=['POST', 'GET'])
@login_required
def patient_details(id):
    """Display the full patient details form for an existing user."""
    patient = Patient.query.get(id)
    form = PatientForm(obj=patient)

    if request.method == 'POST' and form.validate_on_submit():
        update_patient(patient, form, request.files)
        db.session.commit()
        patient.update_stats()
        return render_template(
            'patient_details.html',
            patient=patient,
            form=form,
            save_message=True
        )
    else:
        if request.method == 'GET':
            # If this patient has a referral to the current organization in SENT status,
            # update it to RECEIVED
            sent_referrals = [
                r for r in patient.referrals
                if r.to_service_id == current_user.service_id
                and r.in_sent_status()
            ]
            for referral in sent_referrals:
                referral.mark_received()
            if sent_referrals:
                db.session.commit()

            patient.update_stats()

        return render_template(
            'patient_details.html',
            patient=patient,
            form=form,
            save_message=False
        )


def update_patient(patient, form, files):
    """Update a patient record with information from submitted form."""
    for field_name, class_name in [
        ('income_sources', IncomeSource),
        ('phone_numbers', PhoneNumber),
        ('addresses', Address),
        ('emergency_contacts', EmergencyContact),
        ('household_members', HouseholdMember),
        ('employers', Employer),
        ('document_images', DocumentImage)
    ]:
        if form[field_name]:
            # If the last row in a many-to-one section doesn't have any data, don't save it
            if not bool([val for key, val in form[field_name][-1].data.iteritems() if (
                val != ''
                and val is not None
                and key != 'id'
                and not (key in ['state', 'employee'])
                and not (
                    type(val) is FileStorage
                    and val.filename == ''
                )
            )]):
                form[field_name].pop_entry()

            # Add a new child object for each new item in a many-to-one section
            new_row_count = len(form[field_name].entries) - getattr(patient, field_name).count()
            if new_row_count > 0:
                for p in range(new_row_count):
                    getattr(patient, field_name).append(class_name())

            # When a user clicks the delete icon on a many-to-one row, it clears
            # all the data in that row. If any existing rows have no data, delete
            # them from patient object and then from the form.
            for row in form[field_name]:
                if not bool([val for key, val in row.data.iteritems() if (
                    val != ''
                    and val is not None
                    and key != 'id'
                    and not (key in ['state', 'employee'])
                )]):
                    row_index = int(row.name[-1])
                    # Delete from patient object
                    db.session.delete(getattr(patient, field_name)[row_index])
                    # Deletion from form FieldList requires popping all entries
                    # after the one to be removed, then readding them
                    to_re_add = []
                    for _ in range(len(form[field_name].entries) - row_index):
                        to_re_add.append(form[field_name].pop_entry())
                    to_re_add.pop()
                    for row in to_re_add:
                        form[field_name].append_entry(data=row.data)

    # Upload any new document images
    for index, entry in enumerate(form.document_images):
        if entry.file_name.data and entry.file_name.data.filename:
            entry.file_name.data = upload_file(entry.file_name.data)
        else:
            entry.file_name.data = patient.document_images[index].file_name

    # Populate the patient object with all the updated info
    form.populate_obj(patient)
    return


@screener.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete(id):
    """Hard delete a patient. Soft-deleting is usually a better idea."""
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('screener.index'))


@screener.route('/document_image/<image_id>')
@login_required
def document_image(image_id):
    """Display an uploaded document image."""
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
    """Serve a document image file."""
    return send_document_image(filename)


@screener.route('/new_prescreening', methods=['POST', 'GET'])
@login_required
def new_prescreening():
    """Display the page that allows the user to select which services
    to pre-screen for.
    """
    if request.method == 'POST':
        session['service_ids'] = request.form.getlist('services')
        return redirect(url_for('screener.prescreening_basic'))
    services = Service.query.all()
    return render_template('new_prescreening.html', services=services)


@screener.route('/prescreening_basic', methods=['POST', 'GET'])
@login_required
def prescreening_basic():
    """Page for inputting basic prescreening requirements--
    household size, income, insurance status.
    """
    form = PrescreenForm()
    if form.validate_on_submit():
        session['household_size'] = form.household_size.data
        session['household_income'] = form.household_income.data
        session['has_health_insurance'] = form.has_health_insurance.data
        session['is_eligible_for_medicaid'] = form.eligible_for_medicaid.data
        return redirect(url_for('screener.prescreening_results'))
    else:
        return render_template('prescreening_basic.html', form=form)


@screener.route('/prescreening_results')
@login_required
def prescreening_results():
    """Page with patient's prescreening results: which services she qualifies for and why,
    which sliding scale she'll fall into, and sample prices.
    """
    fpl = calculate_fpl(session['household_size'], int(session['household_income']) * 12)
    return render_template(
        'prescreening_results.html',
        services=calculate_pre_screen_results(
            fpl=fpl,
            has_health_insurance=session['has_health_insurance'],
            is_eligible_for_medicaid=session['is_eligible_for_medicaid'],
            service_ids=session['service_ids']
        ),
        household_size=session['household_size'],
        household_income=int(session['household_income']) * 12,
        fpl=fpl,
        has_health_insurance=session['has_health_insurance'],
        is_eligible_for_medicaid=session['is_eligible_for_medicaid']
    )


@screener.route('/patient_print/<patient_id>')
@login_required
def patient_print(patient_id):
    """Format the patient details page for printing."""
    patient = Patient.query.get(patient_id)
    form = PatientForm(obj=patient)
    return render_template('patient_details.html', patient=patient, form=form)


@screener.route('/patient_history/<patient_id>')
@login_required
def patient_history(patient_id):
    """Display all past edits to the patient's information"""
    patient = Patient.query.get(patient_id)
    patient.update_stats()

    history = ActionLog.query.\
        filter(or_(
            and_(
                ActionLog.row_id == patient_id,
                ActionLog.table_name == 'patient'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.phone_numbers]),
                ActionLog.table_name == 'phone_number'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.addresses]),
                ActionLog.table_name == 'address'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.emergency_contacts]),
                ActionLog.table_name == 'emergency_contact'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.employers]),
                ActionLog.table_name == 'employer'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.document_images]),
                ActionLog.table_name == 'document_image'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.income_sources]),
                ActionLog.table_name == 'income_source'
            ),
            and_(
                ActionLog.row_id.in_([p.id for p in patient.household_members]),
                ActionLog.table_name == 'household_member'
            )
        )).\
        order_by(ActionLog.action_timestamp.desc())
    # Filter out history entries that are only last modified/last modified by changes
    history = [i for i in history if not (
        i.changed_fields
        and set(i.changed_fields).issubset(['last_modified', 'last_modified_by'])
    )]

    services = dict((x.id, x) for x in Service.query.all())

    readable_names = dict(
        (column.name, column.info) for column in (
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
    )

    return render_template(
        'history.html',
        patient=patient,
        history=history,
        services=services,
        readable_names=readable_names
    )


@screener.route('/patient_share/<patient_id>')
@login_required
def patient_share(patient_id):
    """Displays the 'Share Patient' page, which includes prescreening
    results and allows users to send referrals.
    """
    patient = Patient.query.get(patient_id)
    patient.update_stats()
    services = Service.query.all()
    # Get ids of services where the patient already has open referrals,
    # to prevent user from sending duplicates.
    open_referral_service_ids = [
        r.to_service_id for r in patient.referrals
        if (r.in_sent_status() or r.in_received_status())
    ]

    return render_template(
        'patient_share.html',
        patient=patient,
        current_user=current_user,
        services=calculate_pre_screen_results(
            fpl=patient.fpl_percentage,
            has_health_insurance=patient.insurance_status,
            is_eligible_for_medicaid="",
            service_ids=[s.id for s in services]
        ),
        household_size=patient.household_members.count() + 1,
        household_income=patient.total_annual_income,
        fpl=patient.fpl_percentage,
        has_health_insurance=patient.insurance_status,
        is_eligible_for_medicaid="",
        referral_buttons=True,
        open_referral_service_ids=open_referral_service_ids
    )


@screener.route('/add_referral', methods=["POST"])
@login_required
def add_referral():
    """Adds new referral to the database. Called when user clicks
    'Send Referral' button."""
    referral = PatientReferral(
        patient_id=request.form['patient_id'],
        from_app_user_id=request.form['app_user_id'],
        to_service_id=request.form['service_id'],
        status='SENT'
    )
    db.session.add(referral)
    db.session.commit()
    return jsonify()


@screener.route('/patient_screening_history/<patient_id>', methods=['POST', 'GET'])
@login_required
def patient_screening_history(patient_id):
    """Display a patient's past referrals and screening results, and a form
    to enter new screening results.
    """
    patient = Patient.query.get(patient_id)
    patient.update_stats()
    form = ScreeningResultForm()
    sliding_scale_options = SlidingScale.query.filter(
        SlidingScale.service_id == current_user.service_id
    )
    # Add the current organization's sliding scale options to the dropdown
    form.sliding_scale_id.choices = [
        (str(option.id), option.scale_name) for option in sliding_scale_options
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
    """Display the initial landing page, which lists patients in the
    network and allows users to search and filter them.
    """
    session.clear()
    all_patients = Patient.query.all()
    # Get patients created or updated in the last week
    recently_updated = Patient.query.filter(or_(
        Patient.last_modified > datetime.date.today() - datetime.timedelta(days=7),
        Patient.created > datetime.date.today() - datetime.timedelta(days=7)
    ))
    # Get patients with open referrals at the current user's organization
    open_referrals = Patient.query.filter(
        Patient.referrals.any(and_(
            PatientReferral.to_service_id == current_user.service_id,
            PatientReferral.status.in_(('SENT', 'RECEIVED'))
        ))
    )
    # Get referrals the current user created
    your_referrals = Patient.query.filter(
        Patient.referrals.any(
            PatientReferral.from_app_user_id == current_user.id
        )
    )

    return render_template(
        'index.html',
        all_patients=all_patients,
        recently_updated=recently_updated,
        open_referrals=open_referrals,
        your_referrals=your_referrals
    )


@screener.route('/user/<user_id>')
@login_required
def user(user_id):
    """Display the profile page for a single user."""
    user = AppUser.query.get(user_id)
    return render_template('user_profile.html', user=user)


@screener.route('/service/<service_id>')
@login_required
def service(service_id):
    """Display the profile page for a service organization."""
    service = translate_object(
        Service.query.get(service_id),
        current_app.config['BABEL_DEFAULT_LOCALE']
    )
    return render_template('service_profile.html', service=service)


#########################################
# Development-only routes
#########################################

@screener.route('/template_prototyping/')
def template_prototyping():
    """This is a dev-only route for prototyping fragments of other templates without touching
    them. The url should not be linked anywhere, and ideally it should be not be
    accessible in the deployed version."""
    return render_template('template_prototyping.html')


@screener.route('/mockup')
@login_required
def mockup():
    return render_template('MOCKUPS.html')
