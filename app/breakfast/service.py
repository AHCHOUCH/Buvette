"""Business services for breakfast ordering."""
from decimal import Decimal
from app.models import BreakfastOrder, BreakfastOrderItem, BreakfastProduct
from app.repositories.core import BreakfastRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_DEBIT, REFERENCE_BREAKFAST
from app.utils.formatting import normalize_money

class BreakfastService:
    def __init__(self, session): self.session=session; self.repo=BreakfastRepository(session)
    def products(self, active_only=True, product_types=None):
        q=self.session.query(BreakfastProduct)
        if active_only: q=q.filter_by(is_active=True)
        if product_types: q=q.filter(BreakfastProduct.product_type.in_(product_types))
        return q.order_by(BreakfastProduct.name).all()
    def get_product(self, product_id): return self.repo.product(product_id)
    def save_product(self, name, price, is_active=True, product=None, product_type='breakfast'):
        name=(name or '').strip(); product_type=(product_type or 'breakfast').strip()
        if product_type not in {'breakfast','drink','lunch_extra'}: product_type='breakfast'
        if not name: raise ValueError('error.required')
        price=normalize_money(price)
        if price <= 0: raise ValueError('error.invalid_amount')
        existing=self.session.query(BreakfastProduct).filter(BreakfastProduct.is_active.is_(True), BreakfastProduct.product_type==product_type, BreakfastProduct.name.ilike(name)).first()
        if existing and (not product or existing.id != product.id): raise ValueError('flash.product_duplicate')
        product=product or BreakfastProduct(); product.name=name; product.price=price; product.is_active=is_active; product.product_type=product_type
        self.repo.save_product(product); return product
    def archive_product(self, product):
        from app.models import utcnow
        product.is_active=False; product.archived_at=utcnow(); self.session.add(product); return product
    def can_delete_product(self, product):
        from app.models import BreakfastOrderItem, LunchOrderItem
        return not self.session.query(BreakfastOrderItem.id).filter_by(product_id=product.id).first() and not self.session.query(LunchOrderItem.id).filter_by(product_id=product.id).first()
    def delete_product(self, product):
        if not self.can_delete_product(product): raise ValueError('error.delete_blocked')
        self.session.delete(product)
    def create_order(self, client_id, quantities, notes='', user_id=None):
        items=[]; total=Decimal('0.00')
        for product_id, qty in quantities.items():
            try: qty=int(qty or 0); pid=int(product_id)
            except (TypeError, ValueError): continue
            if qty <= 0: continue
            product=self.repo.product(pid)
            if not product or not product.is_active: continue
            line=normalize_money(product.price * qty); total += line
            items.append(BreakfastOrderItem(product=product, product_name=product.name, unit_price=product.price, quantity=qty, line_total=line))
        if not items: raise ValueError('error.required')
        order=BreakfastOrder(client_id=client_id, total_amount=normalize_money(total), notes=notes, items=items)
        self.repo.save_order(order); self.session.flush()
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_DEBIT, amount=order.total_amount, reference_type=REFERENCE_BREAKFAST, reference_id=order.id, description=f'Breakfast order #{order.id}', created_by_user_id=user_id)
        return order
