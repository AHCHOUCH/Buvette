"""Apply SQL migrations to the configured SQLite development database."""
from pathlib import Path
import sqlite3
from app import create_app

app = create_app()
uri = app.config['SQLALCHEMY_DATABASE_URI']
if not uri.startswith('sqlite:///'):
    raise SystemExit('scripts/apply_migrations.py is intended for SQLite development databases only.')
db_path = Path(uri.removeprefix('sqlite:///'))
if not db_path.is_absolute():
    db_path = Path(app.instance_path) / db_path
migrations = sorted(Path('migrations').glob('*.sql'))
with sqlite3.connect(db_path) as conn:
    for migration in migrations:
        conn.executescript(migration.read_text(encoding='utf-8'))
        print(f'Applied {migration}')
print(f'Database migrated: {db_path}')
