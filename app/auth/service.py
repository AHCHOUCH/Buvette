"""Database-backed authentication services."""
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User, utcnow
from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER

ROLE_NAMES = {ROLE_ADMIN: 'Administrator', ROLE_CASHIER: 'Cashier'}

def normalize_username(username): return (username or '').strip().lower()

def authenticate(username: str, password: str):
    user = User.query.filter_by(username=normalize_username(username)).first()
    if user and user.is_active and check_password_hash(user.password_hash, password or ''):
        user.last_login_at = utcnow(); db.session.add(user); return user
    return None

def get_user_by_id(user_id: str):
    try: return db.session.get(User, int(user_id))
    except Exception: return None

def available_demo_users(): return ('administrator','cashier')

def set_password(username: str, password: str) -> None:
    user = User.query.filter_by(username=normalize_username(username)).first()
    if user and password:
        user.password_hash = generate_password_hash(password); db.session.add(user)

def create_user(username, password, full_name, role=ROLE_CASHIER, active=True, user=None):
    username=normalize_username(username); full_name=(full_name or username).strip()
    if role not in (ROLE_ADMIN, ROLE_CASHIER): raise ValueError('Invalid role.')
    existing=User.query.filter_by(username=username).first()
    if existing and (not user or existing.id != user.id): raise ValueError('Username already exists.')
    user = user or User(username=username)
    user.full_name=full_name; user.display_name=full_name; user.role=role; user.is_active=active
    if password: user.password_hash=generate_password_hash(password)
    if not user.password_hash: raise ValueError('Password is required.')
    db.session.add(user); return user
