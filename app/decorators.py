from functools import wraps
from flask import abort
from flask.ext.login import current_user
from app.models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def view_all_patients_required(f):
    return permission_required(Permission.VIEW_ALL_PATIENTS)(f)


def view_admin_pages_required(f):
    return permission_required(Permission.VIEW_ADMIN_PAGES)(f)
