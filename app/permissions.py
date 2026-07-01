from functools import wraps
from flask import abort, request
from flask_login import current_user, login_required
from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER

ADMIN_PERMISSIONS = {'dashboard','clients','breakfast','lunch','suppliers','charges','payments','ledger','settings','users','logs','delete'}
CASHIER_PERMISSIONS = {'dashboard','breakfast','lunch','payments','clients_basic'}

def has_permission(permission):
    if not current_user.is_authenticated:
        return False
    if current_user.role == ROLE_ADMIN:
        return permission in ADMIN_PERMISSIONS
    if current_user.role == ROLE_CASHIER:
        return permission in CASHIER_PERMISSIONS
    return False

def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if not has_permission(permission):
                try:
                    from app.audit import log_audit
                    log_audit('authorization.failure', 'Route', None, f'Unauthorized access to {request.path}', severity='WARNING')
                except Exception:
                    pass
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
