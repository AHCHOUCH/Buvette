"""Business services for lunch menus and charging."""
from datetime import date
from app.models import LunchMenu, LunchOrder
from app.repositories.core import LunchRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_DEBIT, REFERENCE_LUNCH
from app.utils.formatting import normalize_money

class LunchService:
    def __init__(self, session): self.session=session; self.repo=LunchRepository(session)
    def menus(self): return self.repo.menus()
    def save_menu(self, weekday, name, price, is_active=True):
        weekday=int(weekday); name=(name or '').strip()
        if weekday < 0 or weekday > 6: raise ValueError('Invalid weekday.')
        if not name: raise ValueError('Menu name is required.')
        menu=self.repo.menu_for_weekday(weekday) or LunchMenu(weekday=weekday)
        menu.name=name; menu.price=normalize_money(price); menu.is_active=is_active
        if menu.price < 0: raise ValueError('Price cannot be negative.')
        self.repo.save_menu(menu); return menu
    def charge_today(self, client_id, service_date=None, user_id=None):
        service_date=service_date or date.today(); menu=self.repo.menu_for_weekday(service_date.weekday())
        if not menu or not menu.is_active: raise ValueError('No active lunch menu is configured for today.')
        order=LunchOrder(client_id=client_id, menu=menu, service_date=service_date, menu_name=menu.name, amount=menu.price)
        self.repo.save_order(order); self.session.flush()
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_DEBIT, amount=order.amount, reference_type=REFERENCE_LUNCH, reference_id=order.id, description=f'Lunch: {order.menu_name}', created_by_user_id=user_id)
        return order
