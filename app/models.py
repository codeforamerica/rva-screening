from app import db

class Patient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(64))
  middlename = db.Column(db.String(64), nullable=True)
  lastname = db.Column(db.String(64))
  dob = db.Column(db.Date())
  phonenumber1 = db.Column(db.String(32), nullable=True)
  phonenumber2 = db.Column(db.String(32), nullable=True)
  documentimages = db.relationship('DocumentImage', backref='patient', lazy='dynamic')
  householdsize = db.Column(db.Integer, nullable=True)
  householdincome = db.Column(db.Integer, nullable=True)

  def __init__(self, **fields): 
    self.__dict__.update(fields)

class DocumentImage(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  patientid = db.Column(db.Integer, db.ForeignKey("patient.id"))
  filename = db.Column(db.String(64))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64))
  password = db.Column(db.String(128))
  authenticated = db.Column(db.Boolean, default=False)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.email


