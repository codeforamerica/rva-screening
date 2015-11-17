import datetime
from StringIO import StringIO
from werkzeug.datastructures import FileStorage
from tests.unit.test_base import BaseTestCase
from tests.unit.screener.utils import (
    get_user,
    get_service,
    get_patient
)
from app.models import AppUser, Service, ServiceTranslation, Patient
from app.prescreening import calculate_fpl, calculate_pre_screen_results
from app.utils import translate_object
import add_data.add_service_data as add_service_data


class TestScreener(BaseTestCase):

    def setUp(self):
        super(TestScreener, self).setUp()
        self.test_user = get_user()

    def test_login_logout(self):
        """Test logging in and out."""
        app_user = get_user()
        self.login('richmond@codeforamerica.org', 'password')
        self.assert_template_used('index.html')
        self.logout()
        self.assertEquals(app_user.authenticated, False)
        self.login('richmond@codeforamerica.org', 'badpassword')
        self.assert_template_used('security/login_user.html')
        self.assertEquals(app_user.authenticated, False)

    def test_index(self):
        """Test that the index page works as expected."""
        response = self.login()
        response = self.client.get('/index')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_add_patient(self):
        """Test that adding a patient works as expected."""
        # Check that the new patient page loads as expected.
        self.login()
        response = self.client.get('/new_patient')
        self.assert200(response)
        self.assert_template_used('patient_details.html')

        # Check that you can't save a new patient without a name
        response = self.client.post('/new_patient', data=dict(
            gender='',
            has_prescription_coverage_yn='N',
            eligible_for_vets_benefits_yn='N'
        ))
        self.assert200(response)
        self.assertEquals(len(Patient.query.all()), 0)

        # Check that a new patient saves
        response = self.client.post('/new_patient', data=dict(
            first_name='John',
            last_name='Richmond',
            dob='1950-01-01',
            ssn='111-11-1111',
            gender='',
            has_prescription_coverage_yn='N',
            eligible_for_vets_benefits_yn='N'
        ), follow_redirects=True)

        saved_patient = Patient.query.first()
        self.assertEquals(
            saved_patient.first_name,
            'John'
        )
        self.assertEquals(
            saved_patient.last_name,
            'Richmond'
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
        """Test that updating an existing patient works as expected."""
        self.login()
        patient = get_patient()

        # Check that the patient details page loads for an existing patient
        response = self.client.get('/patient_details/{}'.format(patient.id))
        self.assert200(response)
        self.assert_template_used('patient_details.html')

        # Check that updates to the patient save, including many-to-one fields
        post_data = dict(
            first_name='James',
            last_name='Richmond',
            dob='1950-12-12',
            ssn='222-22-2222',
            medical_home="CAHN",
            email='test@test.com',
            has_transport_yn='N',
            gender='M',
            transgender='No',
            race='AA',
            ethnicity='NHL',
            languages=['EN', 'ES'],
            has_interpreter_yn='N',
            education_level='High school',
            marital_status='MAR',
            veteran_yn='N',
            housing_status='REN',
            # years_living_in_area='5',
            # months_living_in_area='1',
            time_in_area='LESS THAN 6',
            city_or_county_of_residence='Richmond',
            temp_visa_yn='N',
            student_status='Not a student',
            employment_status='FT',
            spouse_employment_status='PT',
            years_unemployed='0',
            months_unemployed='6',
            spouse_years_unemployed='1',
            spouse_months_unemployed='11',
            years_at_current_employer='LESS',
            spouse_years_at_current_employer='LESS',
            last_healthcare='Last year at VCU ED',
            insurance_status='N',
            coverage_type='VCC',
            has_prescription_coverage_yn='N',
            has_vcc='Y',
            eligible_insurance_types='NE',
            applied_for_vets_benefits_yn='N',
            eligible_for_vets_benefits_yn='N',
            applied_for_medicaid_yn='N',
            medicaid_date_effective='2015-01-01',
            applied_for_ssd_yn='N',
            ssd_date_effective='1999-12-12',
            care_due_to_accident_yn='N',
            accident_work_related_yn='N',
            filed_taxes_yn='N',
            claimed_as_dependent_yn='N',
            how_food_and_shelter='Stay with sister',
            how_other_expenses='Gets money from father'
        )
        post_data['phone_numbers-0-phone_number'] = '(111) 111-1111'
        post_data['phone_numbers-0-number_description'] = 'CELL'
        post_data['phone_numbers-1-phone_number'] = '(222) 222-2222'
        post_data['phone_numbers-1-number_description'] = 'HOME'
        post_data['addresses-0-address1'] = '1 Main St.'
        post_data['addresses-0-address2'] = 'Apt. 1'
        post_data['addresses-0-city'] = 'Richmond'
        post_data['addresses-0-state'] = 'VA'
        post_data['addresses-0-zip'] = '11111'
        post_data['addresses-0-address_description'] = 'OWN'
        post_data['addresses-1-address1'] = '1 Maple St.'
        post_data['addresses-1-address2'] = ''
        post_data['addresses-1-city'] = 'Richmond'
        post_data['addresses-1-state'] = 'VA'
        post_data['addresses-1-zip'] = '11111'
        post_data['addresses-1-address_description'] = 'RELATIVE'
        post_data['emergency_contacts-0-full_name'] = 'Jane Johnson'
        post_data['emergency_contacts-0-relationship'] = 'mother'
        post_data['emergency_contacts-0-phone_number'] = '(111) 111-1111'
        post_data['emergency_contacts-1-full_name'] = 'Mary Richmond'
        post_data['emergency_contacts-1-relationship'] = 'sister'
        post_data['emergency_contacts-1-phone_number'] = '(222) 222-2222'
        post_data['household_members-0-full_name'] = 'Michael Richmond'
        post_data['household_members-0-dob'] = '2000-12-12'
        post_data['household_members-0-ssn'] = '999-99-9999'
        post_data['household_members-0-relationship'] = 'son'
        post_data['household_members-1-full_name'] = '11111'
        post_data['household_members-1-dob'] = '2006-02-28'
        post_data['household_members-1-ssn'] = '888-88-8888'
        post_data['household_members-1-relationship'] = 'Emily Richmond'
        post_data['income_sources-0-source'] = 'job'
        post_data['income_sources-0-monthly_amount'] = '1000'
        post_data['income_sources-1-source'] = 'food stamps'
        post_data['income_sources-1-monthly_amount'] = '200'
        post_data['employers-0-employer_name'] = 'Target'
        post_data['employers-0-phone_number'] = '(111) 111-1111'
        post_data['employers-0-employee'] = 'Patient'
        post_data['employers-0-start_date'] = '2014-01-01'
        post_data['employers-1-employer_name'] = 'Walmart'
        post_data['employers-1-phone_number'] = '(222) 222-2222'
        post_data['employers-1-employee'] = 'Spouse'
        post_data['employers-1-start_date'] = '1999-12-12'

        response = self.client.post(
            '/patient_details/{}'.format(patient.id),
            data=post_data,
            follow_redirects=True
        )

        saved_patient = Patient.query.first()

        self.assertEquals(
            saved_patient.first_name,
            'James'
        )
        self.assertEquals(
            saved_patient.last_name,
            'Richmond'
        )
        self.assertEquals(
            saved_patient.dob,
            datetime.date(1950, 12, 12)
        )
        self.assertEquals(
            saved_patient.ssn,
            '222-22-2222'
        )
        self.assertEquals(saved_patient.phone_numbers.count(), 2)
        self.assertEquals(saved_patient.addresses.count(), 2)
        self.assertEquals(saved_patient.emergency_contacts.count(), 2)
        self.assertEquals(saved_patient.household_members.count(), 2)
        self.assertEquals(saved_patient.income_sources.count(), 2)
        self.assertEquals(saved_patient.employers.count(), 2)
        # Check that the user stays on patient details page after saving
        self.assert_template_used('patient_details.html')

        # Check that updated many-to-one fields save correctly
        post_data['phone_numbers-0-phone_number'] = '(333) 333-3333'
        post_data['phone_numbers-0-number_description'] = 'WORK'
        response = self.client.post(
            '/patient_details/{}'.format(patient.id),
            data=post_data,
            follow_redirects=True
        )
        self.assert200(response)
        saved_patient = Patient.query.first()
        self.assertEquals(saved_patient.phone_numbers[0].phone_number, '(333) 333-3333')
        self.assertEquals(saved_patient.phone_numbers[0].number_description, 'WORK')
        self.assert_template_used('patient_details.html')

        # Check that deleting many-to-one fields works as expected
        post_data['phone_numbers-0-phone_number'] = ''
        post_data['phone_numbers-0-number_description'] = ''
        response = self.client.post(
            '/patient_details/{}'.format(patient.id),
            data=post_data,
            follow_redirects=True
        )
        self.assert200(response)
        self.assertEquals(saved_patient.phone_numbers.count(), 1)
        self.assertEquals(saved_patient.phone_numbers[0].phone_number, '(222) 222-2222')
        self.assertEquals(saved_patient.phone_numbers[0].number_description, 'HOME')
        self.assert_template_used('patient_details.html')

    # def test_document_image(self):
    #     """Test that uploading document images works as expected."""
    #     self.login()
    #     patient = get_patient()

    #     # Check that multiple document image uploads save correctly
    #     with open('tests/unit/screener/test_image.jpg', 'rb') as test_image:
    #         img_string_io = StringIO(test_image.read())

    #     post_data = dict(
    #         first_name='James',
    #         last_name='Richmond',
    #         dob='1950-12-12',
    #         gender='',
    #         transgender='',
    #         race='',
    #         ethnicity='',
    #         coverage_type='',
    #         student_status='',
    #         employment_status='',
    #         marital_status='',
    #         housing_status='',
    #         veteran_yn='',
    #         insurance_status='',
    #         spouse_employment_status='',
    #         has_prescription_coverage_yn='N',
    #         eligible_for_vets_benefits_yn='N',
    #         eligible_insurance_types='',
    #         applied_for_ssd_yn='',
    #         accident_work_related_yn='',
    #         has_vcc='',
    #         filed_taxes_yn='',
    #         applied_for_medicaid_yn='',
    #         has_interpreter_yn='',
    #         applied_for_vets_benefits_yn='',
    #         has_transport_yn='',
    #         claimed_as_dependent_yn='',
    #         temp_visa_yn='',
    #         care_due_to_accident_yn=''
    #     )
    #     post_data['document_images-0-file_name'] = FileStorage(img_string_io, filename='test_image.jpg')
    #     post_data['document_images-0-file_description'] = 'Test'
    #     post_data['document_images-1-file_name'] = FileStorage(img_string_io, filename='test_image_2.jpg')
    #     post_data['document_images-1-file_description'] = 'Test 2'

    #     response = self.client.post(
    #         '/patient_details/{}'.format(patient.id),
    #         data=post_data,
    #         follow_redirects=True
    #     )
    #     self.assert200(response)
    #     saved_patient = Patient.query.first()
    #     self.assertEquals(saved_patient.document_images.count(), 2)

    #     # Check that the page that displays the images loads correctly
    #     for image in saved_patient.document_images:
    #         response = self.client.get(
    #             '/document_image/{}'.format(image.id)
    #         )
    #         self.assert200(response)
    #         self.assert_template_used('documentimage.html')

    def test_delete_patient(self):
        """Test that hard-deleting a patient works as expected."""
        user = get_user()
        self.login()
        patient = get_patient(user)
        response = self.client.get('/delete/{}'.format(patient.id), follow_redirects=True)
        self.assert200(response)
        # Check that patient was deleted
        self.assertTrue(Patient.query.get(patient.id).deleted)
        # Check that user is redirected to index page
        self.assert_template_used('index.html')

    def test_new_prescreening(self):
        """Test that the new prescreening page works as expected."""
        response = self.client.get('/new_prescreening')
        self.assert200(response)
        self.assert_template_used('new_prescreening.html')

    def test_patient_history(self):
        """Test that the edit history page works as expected."""
        self.login()
        patient = get_patient()
        response = self.client.get('/patient_history/{}'.format(patient.id))
        self.assert200(response)
        self.assert_template_used('patient_history.html')

    def test_patient_share(self):
        """Test that the share patient page works as expected."""
        self.login()
        patient = get_patient()
        response = self.client.get('/patient_share/{}'.format(patient.id))
        self.assert200(response)
        self.assert_template_used('patient_share.html')

    def test_add_referral(self):
        """Test that adding a referral works as expected."""
        self.login()
        user = AppUser.query.first()
        patient = get_patient()
        response = self.client.post('/add_referral', data=dict(
            patient_id=patient.id,
            app_user_id=user.id,
            service_id='1',
            notes='this is a note'
        ), follow_redirects=True)
        self.assert200(response)
        referral = Patient.query.first().referrals[0]
        self.assertEquals(referral.from_app_user_id, user.id)
        self.assertEquals(referral.to_service_id, 1)

    def test_user(self):
        """Test that the user profile page works as expected."""
        user = get_user()
        response = self.client.get('/user/{}'.format(user.id))
        self.assert200(response)
        self.assert_template_used('user_profile.html')

    def test_service(self):
        """Test that the service profile page works as expected."""
        service = get_service()
        response = self.client.get('/service/{}'.format(service.id))
        self.assert200(response)
        self.assert_template_used('service_profile.html')

    def test_fpl_calculation(self):
        """Test that calculating a patient's Federal Poverty Level percentage
        works as expected.
        """
        self.assertEquals(calculate_fpl(8, 40890), 100)
        self.assertEquals(calculate_fpl(1, 0), 0)

    def test_prescreening_basic(self):
        """Test that the prescreening input page works as expected."""
        # Make sure the prescreening input page loads
        response = self.client.get('/prescreening_basic')
        self.assert200(response)
        self.assert_template_used('prescreening_basic.html')

        # Make sure submitting the form works
        response = self.client.post('/prescreening_basic', data=dict(
            household_size='5',
            household_income='1000',
            has_health_insurance='N',
            is_eligible_for_medicaid='N'
        ))
        self.assertRedirects(response, '/prescreening_results')

    def test_calculate_pre_screen_results(self):
        """Test that calculating prescreening results works as expected."""
        add_service_data.main(self.app)
        daily_planet = Service.query.filter(Service.name == 'Daily Planet').first()
        result = calculate_pre_screen_results(
            fpl=0,
            has_health_insurance='no',
            is_eligible_for_medicaid='no',
            service_ids=[daily_planet.id]
        )[0]

        self.assertEquals(result['name'], daily_planet.name)
        self.assertEquals(result['eligible'], True)
        self.assertEquals(result['fpl_cutoff'], daily_planet.fpl_cutoff)
        self.assertEquals(result['fpl_eligible'], True)
        self.assertEquals(result['uninsured_only_yn'], daily_planet.uninsured_only_yn)
        self.assertEquals(
            result['medicaid_ineligible_only_yn'],
            daily_planet.medicaid_ineligible_only_yn
        )
        self.assertEquals(
            result['residence_requirement_yn'],
            daily_planet.residence_requirement_yn
        )
        self.assertEquals(
            result['time_in_area_requirement_yn'],
            daily_planet.time_in_area_requirement_yn
        )
        self.assertEquals(result['sliding_scale'], 'Nominal')
        self.assertEquals(result['sliding_scale_range'], 'between 0% and 100%')
        self.assertEquals(result['id'], daily_planet.id)

    def test_patient_screening_history(self):
        """Test that the patient referral/screening history page works as expected."""
        add_service_data.main(self.app)
        user = get_user()
        user.service = Service.query.filter(Service.name == 'Daily Planet').first()
        self.login()
        patient = get_patient()

        # Make sure the page loads as expected
        response = self.client.get('/patient_screening_history/{}'.format(patient.id))
        self.assert200(response)
        self.assert_template_used('patient_screening_history.html')

    def test_patient_overview(self):
        """Test that the patient overview and screening result page works as expected."""
        add_service_data.main(self.app)
        user = get_user()
        user.service = Service.query.filter(Service.name == 'Daily Planet').first()
        self.login()
        patient = get_patient(user)

        # Make sure the page loads as expected
        response = self.client.get('/patient_overview/{}'.format(patient.id))
        self.assert200(response)
        self.assert_template_used('patient_overview.html')

        # Make sure you can save a new screening result
        response = self.client.post(
            '/patient_overview/{}'.format(patient.id),
            data=dict(
                eligible_yn='Y',
                sliding_scale_id=user.service.sliding_scales[0].id,
                notes='Test'
            ),
            follow_redirects=True
        )

        self.assert200(response)
        # User should stay on the same page after saving
        self.assert_template_used('patient_overview.html')
        screening_result = Patient.query.first().screening_results[0]
        self.assertEquals(screening_result.service_id, user.service_id)
        self.assertEquals(screening_result.eligible_yn, 'Y')
        self.assertEquals(screening_result.sliding_scale_id, user.service.sliding_scales[0].id)
        self.assertEquals(screening_result.notes, 'Test')

    def test_translate_object(self):
        """Test that translating text from the database works as expected."""
        # Test that the object stays the same if no translation exists
        service = Service(
            name='Richmond Clinic',
            description='English description'
        )
        translated_service = translate_object(service, 'es_US')
        self.assertEquals(translated_service.description, 'English description')

        # Test that the object is translated when a translation exists
        service.translations.append(
            ServiceTranslation(
                language_code='es_US',
                description='Spanish description'
            )
        )
        translated_service = translate_object(service, 'es_US')
        self.assertEquals(translated_service.description, 'Spanish description')
