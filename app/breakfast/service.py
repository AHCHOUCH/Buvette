"""Business services for breakfast ordering."""
from decimal import Decimal
from app import db
from app.models import BreakfastOrder, BreakfastOrderItem, BreakfastProduct
from app.repositories.core import BreakfastRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_DEBIT, REFERENCE_BREAKFAST
from app.utils.formatting import normalize_money

class BreakfastService:
    def __init__(self, session): self.session=session; self.repo=BreakfastRepository(session)
    def products(self, active_only=True): return self.repo.products(active_only)
    def save_product(self, name, price, is_active=True, product=None):
        name=(name or '').strip()
        if not name: raise ValueError('Product name is required.')
        existing=self.repo.product_by_name(name)
        if existing and (not product or existing.id != product.id): raise ValueError('A breakfast product with this name already exists.')
        product=product or BreakfastProduct(); product.name=name; product.price=normalize_money(price); product.is_active=is_active
        if product.price < 0: raise ValueError('Price cannot be negative.')
        self.repo.save_product(product); return product
    def create_order(self, client_id, quantities, notes='', user_id=None):
        items=[]; total=Decimal('0.00')
        for product_id, qty in quantities.items():
            qty=int(qty or 0)
            if qty <= 0: continue
            product=self.repo.product(int(product_id))
            if not product or not product.is_active: continue
            line=normalize_money(product.price * qty); total += line
            items.append(BreakfastOrderItem(product=product, product_name=product.name, unit_price=product.price, quantity=qty, line_total=line))
        if not items: raise ValueError('Select at least one breakfast product.')
        order=BreakfastOrder(client_id=client_id, total_amount=normalize_money(total), notes=notes, items=items)
        self.repo.save_order(order); self.session.flush()
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_DEBIT, amount=order.total_amount, reference_type=REFERENCE_BREAKFAST, reference_id=order.id, description=f'Breakfast order #{order.id}', created_by_user_id=user_id)
        return order
