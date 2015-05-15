# -*- coding: utf-8 -*-

import boto.s3
from app.models import DocumentImage
from boto.s3.connection import S3Connection
from werkzeug import secure_filename
from flask import current_app, send_file, send_from_directory, redirect

def send_document_image(file_name):
    if current_app.config['SCREENER_ENVIRONMENT'] == 'prod':
        # conn = S3Connection(
        #     aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        #     aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        # )
        # bucket = conn.get_bucket(current_app.config['S3_BUCKET_NAME'])
        # key = bucket.get_key('/'.join([current_app.config['S3_FILE_UPLOAD_DIR'], file_name]))

        # send_file(
        #     key.get_file(file_name)
        # )
        pass
    else:
        return send_from_directory(os.path.join(
            app.config['PROJECT_ROOT'],
            app.config['UPLOAD_FOLDER']),
            file_name
        )

def upload_file(file):
    if allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        if current_app.config['SCREENER_ENVIRONMENT'] == 'prod':
            conn = S3Connection(
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
            )
            bucket = conn.get_bucket(current_app.config['S3_BUCKET_NAME'])
            _file = bucket.new_key('/'.join([current_app.config['S3_FILE_UPLOAD_DIR'], file_name]))
            _file.set_contents_from_file(file)
            _file.set_acl('public-read')
        else:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)

        return file_name

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config.get('ALLOWED_EXTENSIONS')
