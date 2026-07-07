"""Business services for settings."""
from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.repositories.core import SettingsRepository
from app.utils.formatting import normalize_money

DEFAULTS = {
    "organization_name": "Buvette Manager",
    "organization_short_name": "",
    "logo_path": "",
    "primary_color": "#2f6f73",
    "secondary_color": "#eef2f4",
    "accent_color": "#0d6efd",
    "header_background_color": "#2f6f73",
    "sidebar_background_color": "#eaf3f3",
    "button_color": "#2f6f73",
    "login_background_color": "#f6f7f9",
    "footer_text": "",
    "debt_warning_default": "50.00",
    "currency": "DH",
}
IDENTITY_KEYS = tuple(DEFAULTS.keys())
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "svg"}

class SettingsService:
    def __init__(self, session): self.session=session; self.repo=SettingsRepository(session)
    def get(self, key): return self.repo.get(key, DEFAULTS.get(key, ""))
    def all(self): return {key: self.get(key) for key in DEFAULTS}
    def identity(self):
        values=self.all(); values['organization_name']=(values.get('organization_name') or DEFAULTS['organization_name']).strip() or DEFAULTS['organization_name']
        values['currency']=(values.get('currency') or DEFAULTS['currency']).strip() or DEFAULTS['currency']
        return values
    def save_general(self, data, logo_file: FileStorage | None = None, upload_root: Path | None = None):
        org=(data.get('organization_name') or '').strip()
        if not org: raise ValueError('settings.error.organization_required')
        debt=normalize_money(data.get('debt_warning_default') or 0)
        if debt < 0: raise ValueError('settings.error.debt_negative')
        for key in ('primary_color','secondary_color','accent_color','header_background_color','sidebar_background_color','button_color','login_background_color'):
            value=(data.get(key) or DEFAULTS[key]).strip()
            if value and not HEX_RE.match(value): raise ValueError('settings.error.invalid_color')
        logo_path=data.get('logo_path') or self.get('logo_path')
        if logo_file and logo_file.filename:
            logo_path=self.save_logo(logo_file, upload_root)
        for key in IDENTITY_KEYS:
            if key == 'logo_path': value=logo_path
            elif key == 'debt_warning_default': value=debt
            else: value=(data.get(key) or DEFAULTS.get(key, '')).strip()
            if key == 'currency': value=value or DEFAULTS['currency']
            self.repo.set(key, value)
    def save_logo(self, logo_file: FileStorage, upload_root: Path | None):
        filename=secure_filename(logo_file.filename or '')
        ext=filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in ALLOWED_LOGO_EXTENSIONS: raise ValueError('settings.error.invalid_logo')
        if ext == 'svg':
            sample = logo_file.stream.read(4096).decode('utf-8', errors='ignore').lower()
            logo_file.stream.seek(0)
            if '<script' in sample or 'javascript:' in sample or ' onload=' in sample:
                raise ValueError('settings.error.invalid_logo')
        upload_root=Path(upload_root or 'app/static/uploads')
        upload_root.mkdir(parents=True, exist_ok=True)
        target=upload_root / f"logo-{uuid4().hex}.{ext}"
        logo_file.save(target)
        return f"uploads/{target.name}"
