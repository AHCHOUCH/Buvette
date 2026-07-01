"""Business services for cash payments."""
from app.models import Payment
from app.repositories.core import PaymentRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_CREDIT, REFERENCE_PAYMENT
from app.utils.formatting import normalize_money

class PaymentService:
    def __init__(self, session): self.session=session; self.repo=PaymentRepository(session)
    def create_payment(self, client_id, amount, note='', user_id=None):
        amount=normalize_money(amount)
        if amount <= 0: raise ValueError('Payment amount must be greater than zero.')
        payment=Payment(client_id=client_id, amount=amount, note=note)
        self.repo.save(payment); self.session.flush()
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_CREDIT, amount=amount, reference_type=REFERENCE_PAYMENT, reference_id=payment.id, description=note or 'Cash payment', created_by_user_id=user_id)
        return payment
    def history(self): return self.repo.history()
