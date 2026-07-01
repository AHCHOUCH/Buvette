"""Business services for settings."""
from app.repositories.core import SettingsRepository
from app.utils.formatting import normalize_money

DEFAULTS = {"organization_name": "Company Buvette", "debt_warning_default": "50.00", "currency": "€"}

class SettingsService:
    def __init__(self, session): self.session=session; self.repo=SettingsRepository(session)
    def get(self, key): return self.repo.get(key, DEFAULTS.get(key, ""))
    def all(self): return {key: self.get(key) for key in DEFAULTS}
    def save_general(self, organization_name, debt_warning_default, currency):
        if not (organization_name or '').strip(): raise ValueError('Organization name is required.')
        if normalize_money(debt_warning_default) < 0: raise ValueError('Debt warning default cannot be negative.')
        self.repo.set('organization_name', organization_name.strip()); self.repo.set('debt_warning_default', normalize_money(debt_warning_default)); self.repo.set('currency', (currency or '€').strip() or '€')
