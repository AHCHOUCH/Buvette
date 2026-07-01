from flask import Blueprint, render_template, request
from app.models import AuditLog
from app.permissions import permission_required
logs_bp=Blueprint('logs', __name__, url_prefix='/logs')
@logs_bp.get('/')
@permission_required('logs')
def index():
    q=AuditLog.query
    if request.args.get('severity'): q=q.filter_by(severity=request.args['severity'])
    if request.args.get('action'): q=q.filter(AuditLog.action.ilike('%'+request.args['action']+'%'))
    if request.args.get('entity_type'): q=q.filter_by(entity_type=request.args['entity_type'])
    return render_template('logs/index.html', logs=q.order_by(AuditLog.timestamp.desc()).limit(200).all())
