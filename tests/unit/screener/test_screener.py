import datetime
from tests.unit.test_base import BaseTestCase
from app.models import AppUser, Service, Patient
from app import bcrypt, db

class TestScreener(BaseTestCase):

  def setUp(self):
    super(TestScreener, self).setUp()
    self.test_user = self.get_test_user()

  def get_test_user(self):
    existing_user = AppUser.query.filter(AppUser.email=='richmond@codeforamerica.org').first()
    if not existing_user:
      return self.insert_test_user()

    return existing_user

  def insert_test_user(self):
    service = self.get_test_service()
    app_user = AppUser(
      email='richmond@codeforamerica.org',
      password=bcrypt.generate_password_hash('password'),
      service = service
    )
    db.session.add(app_user)
    db.session.commit()
    return app_user

  def get_test_service(self):
    existing_service = Service.query.first()
    if not existing_service:
      return self.insert_test_service()
    
    return existing_service

  def insert_test_service(self):
    service = Service(
      name='Richmond Clinic'
    )
    db.session.add(service)
    db.session.commit()
    return service

  def get_test_patient(self):
    existing_patient = Patient.query.first()
    if not existing_patient:
      return self.insert_test_patient()
    
    return existing_patient

  def insert_test_patient(self):
    service = self.get_test_service()
    patient = Patient(
      first_name = 'John Richmond',
      dob = '1950-01-01',
      ssn = '111-11-1111'
    )
    patient.services.append(service)
    db.session.add(patient)
    db.session.commit()
    return patient

  def test_login_logout(self):
    app_user = self.get_test_user()
    response = self.login('richmond@codeforamerica.org', 'password')
    self.assert_template_used('index.html')
    response = self.logout()
    self.assertEquals(app_user.authenticated, False)
    response = self.login('richmond@codeforamerica.org', 'badpassword')
    self.assert_template_used('login.html')
    self.assertEquals(app_user.authenticated, False)

  def test_index(self):
    response = self.login()
    response = self.client.get('/')
    self.assert200(response)
    self.assert_template_used('index.html')

  def test_add_patient(self):
    # Check that the patient details page loads as expected
    self.login()
    response = self.client.get('/new_patient')
    self.assert200(response)
    self.assert_template_used('patient_details.html')

    # Check that a new patient saves
    response = self.client.post('/new_patient', data=dict(
      first_name='John Richmond',
      dob='1950-01-01',
      ssn='111-11-1111'
    ), follow_redirects=True)

    saved_patient = Patient.query.first()
    self.assertEquals(
      saved_patient.first_name,
      'John Richmond'
    )
    self.assertEquals(
      saved_patient.dob,
      datetime.date(1950, 1, 1)
    )
    self.assertEquals(
      saved_patient.ssn,
      '111-11-1111'
    )

    # Check that user stays on patient details page after saving
    self.assert_template_used('patient_details.html')

  def test_update_patient(self):
    # Check that the patient details page loads for an existing patient
    self.login()
    patient = self.get_test_patient()
    response = self.client.get('/patient_details/{}'.format(patient.id))
    self.assert200(response)
    self.assert_template_used('patient_details.html')

    # Check that updates save
    response = self.client.post('/patient_details/{}'.format(patient.id), data=dict(
      first_name='James Richmond',
      dob='1950-12-12',
      ssn='222-22-2222'
    ), follow_redirects=True)

    saved_patient = Patient.query.first()
    self.assertEquals(
      saved_patient.first_name,
      'James Richmond'
    )
    self.assertEquals(
      saved_patient.dob,
      datetime.date(1950, 12, 12)
    )
    self.assertEquals(
      saved_patient.ssn,
      '222-22-2222'
    )

    # Check that the user stays on patient details page after saving
    self.assert_template_used('patient_details.html')

  def test_new_prescreening(self):
    # Make sure the new prescreening page loads as expected
    response = self.client.get('/new_prescreening')
    self.assert200(response)
    self.assert_template_used('new_prescreening.html')

  # Test that prescreening returns the right results
  def test_calculate_prescreening_results(self):
    pass

  # Test that the prescreening results page returns the right template
  def test_prescreening_results(self):
    pass

  def test_search_new(self):
    # Make sure the search patients page loads as expected
    self.login()
    response = self.client.get('/search_new')
    self.assert200(response)
    self.assert_template_used('search_new.html')

  def test_patient_print(self):
    # Make sure the print patient page loads as expected
    patient = self.get_test_patient()
    response = self.client.get('/patient_print/{}'.format(patient.id))
    self.assert200(response)
    self.assert_template_used('patient_details.html')

  def test_patient_history(self):
    # Make sure the print history page loads as expected
    patient = self.get_test_patient()
    response = self.client.get('/patient_history/{}'.format(patient.id))
    self.assert200(response)
    self.assert_template_used('history.html')

  def test_patient_share(self):
    # Make sure the share patient page loads as expected
    patient = self.get_test_patient()
    response = self.client.get('/patient_share/{}'.format(patient.id))
    self.assert200(response)
    self.assert_template_used('patient_share.html')

  def test_user(self):
    # Make sure the user profile page loads normally
    user = self.get_test_user()
    response = self.client.get('/user/{}'.format(user.id))
    self.assert200(response)
    self.assert_template_used('user_profile.html')

  def test_service(self):
    # Make sure the service profile page loads normally
    service = self.get_test_service()
    response = self.client.get('/service/{}'.format(service.id))
    self.assert200(response)
    self.assert_template_used('service_profile.html')

  def test_translate_object(self):
    pass


