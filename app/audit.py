import json
from flask import request
from flask_login import current_user
from app import db
from app.models import AuditLog

def log_audit(action, entity_type=None, entity_id=None, description='', severity='INFO', metadata=None, commit=False):
    user_id = None; username = None
    try:
        if current_user.is_authenticated:
            user_id = int(current_user.get_id()); username = current_user.username
    except Exception:
        pass
    entry = AuditLog(user_id=user_id, username_snapshot=username, action=action, entity_type=entity_type, entity_id=entity_id, description=description, ip_address=getattr(request, 'remote_addr', None), user_agent=(request.user_agent.string[:255] if request and request.user_agent else None), severity=severity, metadata_json=(json.dumps(metadata, ensure_ascii=False) if metadata else None))
    db.session.add(entry)
    if commit:
        db.session.commit()
    return entry
