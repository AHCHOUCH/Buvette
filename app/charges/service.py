"""Business services for manual charges."""
from app.models import ManualCharge
from app.repositories.core import ChargeRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_DEBIT, REFERENCE_MANUAL_CHARGE
from app.utils.formatting import normalize_money

CATEGORIES = ("Materials", "Groceries", "Supplies", "Miscellaneous", "Other")

class ChargeService:
    def __init__(self, session): self.session=session; self.repo=ChargeRepository(session)
    def create_charge(self, client_id, amount, category, notes='', user_id=None):
        amount=normalize_money(amount); category=(category or '').strip()
        if amount <= 0: raise ValueError('Amount must be greater than zero.')
        if category not in CATEGORIES: raise ValueError('Invalid charge category.')
        charge=ManualCharge(client_id=client_id, amount=amount, category=category, notes=notes)
        self.repo.save(charge); self.session.flush()
        desc=f'{category} charge' + (f': {notes}' if notes else '')
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_DEBIT, amount=amount, reference_type=REFERENCE_MANUAL_CHARGE, reference_id=charge.id, description=desc, created_by_user_id=user_id)
        return charge
