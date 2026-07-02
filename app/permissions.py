from functools import wraps
from flask import abort, request
from flask_login import current_user, login_required
from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER

ADMIN_PERMISSIONS = {'dashboard.view','clients.manage','breakfast.manage','breakfast.sell','lunch.manage','lunch.sell','suppliers.manage','expenses.manage','payments.manage','ledger.view','reports.view','settings.manage','users.manage','logs.view','dangerous.delete'}
CASHIER_PERMISSIONS = {'dashboard.view_limited','clients.select','clients.view_basic','breakfast.manage','breakfast.sell','lunch.manage','lunch.sell','payments.create'}
ALIASES = {'dashboard':'dashboard.view_limited','clients':'clients.manage','clients_basic':'clients.view_basic','breakfast':'breakfast.manage','lunch':'lunch.manage','suppliers':'suppliers.manage','charges':'expenses.manage','payments':'payments.create','ledger':'ledger.view','settings':'settings.manage','users':'users.manage','logs':'logs.view','delete':'dangerous.delete'}

def normalize_permission(permission):
    return ALIASES.get(permission, permission)

def has_permission(permission):
    if not current_user.is_authenticated:
        return False
    permission = normalize_permission(permission)
    if current_user.role == ROLE_ADMIN:
        return permission in ADMIN_PERMISSIONS or permission in {'dashboard.view_limited','payments.create'}
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
                    log_audit('authorization.failure', 'Route', None, f'Unauthorized access to {request.path}', severity='WARNING', metadata={'permission': normalize_permission(permission)})
                except Exception:
                    pass
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
