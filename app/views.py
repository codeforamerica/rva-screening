from flask import render_template, request,flash, redirect, url_for
from app import app, db
from app.models import Patient
import datetime

@app.route('/add' , methods=['POST', 'GET'])
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
    flash('New patient added!')     
    return redirect(url_for('index'))

  return render_template('add.html')

@app.route('/' )
def index():
  patients = Patient.query.all()    
  return render_template('index.html', patients=patients)
