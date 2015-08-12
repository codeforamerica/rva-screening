# -*- coding: utf-8 -*-

import boto.s3
import os
from boto.s3.connection import S3Connection
from werkzeug import secure_filename
from flask import current_app, send_from_directory


def send_document_image(file_name):
    """Serve an image file."""
    if current_app.config['SCREENER_ENVIRONMENT'] == 'prod':
        # conn = S3Connection(
        #     aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        #     aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        # )
        # bucket = conn.get_bucket(current_app.config['S3_BUCKET_NAME'])
        # key = bucket.get_key(
        #    '/'.join([current_app.config['S3_FILE_UPLOAD_DIR'],
        #    file_name])
        # )

        # send_file(
        #     key.get_file(file_name)
        # )
        pass
    else:
        return send_from_directory(os.path.join(
            current_app.config['PROJECT_ROOT'],
            current_app.config['UPLOAD_FOLDER']),
            file_name
        )


def upload_file(file):
    """Upload a file to AWS or local upload folder."""
    if allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        if current_app.config['SCREENER_ENVIRONMENT'] == 'prod':
            conn = S3Connection(
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
            )
            bucket = conn.get_bucket(current_app.config['S3_BUCKET_NAME'])
            _file = bucket.new_key('/'.join(
                [current_app.config['S3_FILE_UPLOAD_DIR'], file_name]
            ))
            _file.set_contents_from_file(file)
            _file.set_acl('public-read')
        else:
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                file_name
            )
            file.save(file_path)

        return file_name


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
