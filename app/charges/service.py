"""Business services for supplier charges/expenses."""
from app.models import ManualCharge, Supplier
from app.repositories.core import ChargeRepository
from app.utils.formatting import normalize_money
CATEGORIES = ("Groceries", "Bakery", "Vegetables", "Cleaning", "Equipment", "Other")
class SupplierService:
    def __init__(self, session): self.session=session
    def list_suppliers(self, include_archived=False):
        q=self.session.query(Supplier)
        if not include_archived: q=q.filter_by(active=True)
        return q.order_by(Supplier.name).all()
    def get(self, supplier_id): return self.session.get(Supplier, supplier_id)
    def save(self, name, phone='', notes='', active=True, supplier=None):
        name=(name or '').strip()
        if not name: raise ValueError('Supplier name is required.')
        supplier=supplier or Supplier()
        supplier.name=name; supplier.phone=phone; supplier.notes=notes; supplier.active=active
        self.session.add(supplier); return supplier
    def archive(self, supplier): supplier.active=False; self.session.add(supplier); return supplier
    def delete_if_unused(self, supplier):
        if supplier.charges: raise ValueError('Cannot delete supplier with financial history; archive it instead.')
        self.session.delete(supplier)
class ChargeService:
    def __init__(self, session): self.session=session; self.repo=ChargeRepository(session)
    def create_charge(self, supplier_id, amount, category, notes='', user_id=None):
        amount=normalize_money(amount); category=(category or '').strip()
        if amount <= 0: raise ValueError('Amount must be greater than zero.')
        if category not in CATEGORIES: raise ValueError('Invalid charge category.')
        if not self.session.get(Supplier, supplier_id): raise ValueError('Supplier is required.')
        charge=ManualCharge(supplier_id=supplier_id, amount=amount, category=category, notes=notes)
        self.repo.save(charge); self.session.flush()
        return charge
