# -*- coding: utf-8 -*-
import datetime
import json
import pytz

from sqlalchemy import and_
from werkzeug.datastructures import MultiDict, FileStorage

from flask import current_app, session, abort, render_template
from flask.ext.login import login_user, current_user
from flask.ext.security.utils import verify_password
from flask_mail import Message

from app import db, mail
from app.models import (
    AppUser,
    UnsavedForm,
    IncomeSource,
    PhoneNumber,
    Address,
    EmergencyContact,
    HouseholdMember,
    Employer,
    DocumentImage
)


def allowed_file(filename):
    """Check that file extension is allowed."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1] in current_app.config.get('ALLOWED_EXTENSIONS')
    )


def translate_object(obj, language_code):
    """Replace string attributes of an object with translations from
    the database if available."""
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


def login_helper(user_email, password):
    user = AppUser.query.filter(AppUser.email == user_email).first()
    if user and verify_password(
        user.password.encode('utf8'),
        password
    ):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        session.permanent = True
        return True
    else:
        return False


def get_unsaved_form(request, patient, page_name, form_class):
    """If the patient is logging back in after being automatically logged out
    due to inactivity, check whether there's unsaved form data we should restore.
    """
    if request.referrer and request.referrer.find('relogin'):
        unsaved_form = UnsavedForm.query.filter(and_(
            UnsavedForm.patient_id == patient.id,
            UnsavedForm.app_user_id == current_user.id,
            UnsavedForm.page_name.like('%' + page_name + '%')
        )).first()

        if unsaved_form:
            form_dict = {}
            for element in json.loads(unsaved_form.form_json):
                name = element['name']
                form_dict[name] = element['value']
            form_multidict = MultiDict(form_dict)
            form = form_class(formdata=form_multidict)

            # Once we've recreated the form, delete the temp data
            db.session.delete(unsaved_form)
            db.session.commit()

            return form
    return False


def check_patient_permission(patient_id):
    """If the current user is a patient account, check whether they're viewing
    the patient linked to their own account. If not, abort.
    """
    if current_user.is_patient_user() and not current_user.is_current_patient(patient_id):
        abort(403)
    return


def days_from_today(field):
    '''Takes a python date object and returns days from today
    '''
    if isinstance(field, datetime.date):
        return (
            datetime.date(field.year, field.month, field.day) -
            datetime.date.today()
        ).days
    elif isinstance(field, datetime.datetime):
        field = field.replace(tzinfo=pytz.utc)
        return (
            datetime.datetime(field.year, field.month, field.day) -
            datetime.datetime.now(pytz.utc)
        ).days
    else:
        return field


def format_days_from_today(field):
    '''Uses days_from_today to build readable "X days ago"
    '''
    days = days_from_today(field)
    if days == 0:
        return 'Today'
    elif days == 1:
        return '{} day from now'.format(abs(days))
    elif days > 1:
        return '{} days from now'.format(abs(days))
    elif days == -1:
        return '{} day ago'.format(abs(days))
    else:
        return '{} days ago'.format(abs(days))


def send_new_referral_email(service, patient, from_app_user):
    """Send an email to addresses associated with a service, notifying them that they've
    been sent a new referral.
    """
    message = Message(
        "New referral from " + from_app_user.full_name + " at " + from_app_user.service.name
    )
    message.recipients = [e.email for e in service.referral_emails]
    if message.recipients:
        message.html = render_template(
            "emails/referral_notification.html",
            service=service,
            patient=patient,
            from_app_user=from_app_user
        )
        mail.send(message)
    return


def send_referral_comment_email(service, patient, referral, commented_user):
    """Send an email to the user who created a referral, the service emails receiving it,
    and any users who have commented on it in the past, notifying them of a new comment
    on the referral.
    """
    message = Message(
        "New comment on a referral to " + service.name
    )
    service_emails = [e.email for e in service.referral_emails]
    past_commenters = [comment.created_by.email for comment in referral.comments]
    recipient_set = set(service_emails + past_commenters + [referral.from_app_user.email])
    recipient_set.remove(commented_user.email)
    message.recipients = list(recipient_set)

    if message.recipients:
        message.html = render_template(
            "emails/referral_comment.html",
            patient=patient,
            commented_user=commented_user
        )
        mail.send(message)
    return


def send_referral_closed_email(service, patient, from_app_user, closed_user):
    """Send an email to the user who created a referral, notifying them that an eligiblity
    result was entered and the referral closed.
    """
    message = Message(
        "Screening result entered for your referral to " + service.name
    )
    message.recipients = [from_app_user.email]
    if from_app_user.email:
        message.html = render_template(
            "emails/referral_closed.html",
            patient=patient,
            closed_user=closed_user
        )
        mail.send(message)
    return


def remove_blank_rows(form):
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
            remove_blank_rows_helper(form[field_name])


def remove_blank_rows_helper(field):
    # If the last row in a many-to-one section doesn't have any data, don't save it
    if not bool([val for key, val in field[-1].data.iteritems() if (
        val != ''
        and val is not None
        and key != 'id'
        and not (key in ['state', 'employee'])
        and not (
            type(val) is FileStorage
            and val.filename == ''
        )
    )]):
        field.pop_entry()
