from app import db

class Patient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(64))
  middlename = db.Column(db.String(64))
  lastname = db.Column(db.String(64))
  dob = db.Column(db.Date())
  phonenumber1 = db.Column(db.String(32))
  phonenumber2 = db.Column(db.String(32))
   
  def __init__(self, firstname, middlename, lastname, dob, phonenumber1, phonenumber2):
    self.firstname = firstname
    self.middlename = middlename
    self.lastname = lastname
    self.dob = dob
    self.phonenumber1 = phonenumber1
    self.phonenumber2 = phonenumber2 
