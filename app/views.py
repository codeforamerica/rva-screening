from flask import render_template, request,flash, redirect, url_for, g, send_from_directory
from app import app, db, bcrypt, ALLOWED_EXTENSIONS
from app.models import Patient, DocumentImage, User
import datetime
import os
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import login_manager
from werkzeug import secure_filename

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    user = User.query.filter(User.email == request.form['email']).first()
    if user:
      if bcrypt.check_password_hash(user.password, request.form['password']):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
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
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/add' , methods=['POST', 'GET'])
@login_required
def add():
  if request.method == 'POST':
    patient=Patient(
      request.form['firstname'],
      request.form['middlename'],
      request.form['lastname'],
      datetime.datetime.strptime(request.form['dob'], '%m/%d/%Y').date(),
      request.form['phonenumber1'],
      request.form['phonenumber2']
    )
    db.session.add(patient)
    db.session.commit()

    for file in request.files.itervalues():
      if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
      documentImage = DocumentImage(patient.id, filename)
      db.session.add(documentImage)

    db.session.commit()

    flash('New patient added!')     
    return redirect(url_for('index'))

  return render_template('add.html')

@app.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update(id):
  patient = Patient.query.get(id)
  if request.method == 'POST':
    patient.firstname = request.form['firstname'],
    patient.middlename = request.form['middlename'],
    patient.lastname = request.form['lastname'],
    patient.dob = datetime.datetime.strptime(request.form['dob'], '%m/%d/%Y').date(),
    patient.phonenumber1 = request.form['phonenumber1'],
    patient.phonenumber2 = request.form['phonenumber2']
    db.session.commit()
    flash('Patient updated!')
    return redirect(url_for('index'))

  return render_template('update.html', patient=patient)

@app.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete(id):
  patient = Patient.query.get(id)
  db.session.delete(patient)
  db.session.commit()
  flash('Patient deleted!')
  return redirect(url_for('index'))

@app.route('/document_image/<image_id>')
@login_required
def document_image(image_id):
  _image = DocumentImage.query.get(image_id)
  filepath = '/documentimages/' + _image.filename
  return render_template('documentimage.html', filepath=filepath)

@app.route('/documentimages/<filename>')
@login_required
def get_image(filename):
  return send_from_directory(os.path.join(app.config['PROJECT_ROOT'], app.config['UPLOAD_FOLDER']), filename)

@app.route('/' )
@login_required
def index():
  patients = Patient.query.all()    
  print patients[2].documentimages
  return render_template('index.html', patients=patients)
