"""Business services for weekly lunch menus and charging."""
from datetime import date, timedelta
from app.models import DailyMenu, FoodPlate, FoodPlateVariant, LunchMenu, LunchOrder, WeeklyMenu
from app.repositories.core import LunchRepository
from app.ledger.service import LedgerService
from app.utils.constants import LEDGER_DEBIT, REFERENCE_LUNCH
from app.utils.formatting import normalize_money
from app.utils.parsing import parse_required_int

DEFAULT_VARIANTS = (('small', 'small', '20.00'), ('big', 'big', '25.00'))

def week_start_for(day=None):
    day = day or date.today()
    return day - timedelta(days=day.weekday())

class LunchService:
    def __init__(self, session): self.session=session; self.repo=LunchRepository(session)
    def menus(self): return self.session.query(WeeklyMenu).order_by(WeeklyMenu.week_start_date.desc()).all()
    def legacy_menus(self): return self.repo.menus()
    def current_week(self, day=None): return self.session.query(WeeklyMenu).filter_by(week_start_date=week_start_for(day), active=True).first()
    def today_daily_menu(self, day=None):
        day = day or date.today(); week = self.current_week(day)
        if not week: return None
        return self.session.query(DailyMenu).filter_by(weekly_menu_id=week.id, service_date=day, active=True).first()
    def todays_plates(self, day=None):
        daily = self.today_daily_menu(day)
        if not daily: return []
        return self.session.query(FoodPlate).filter_by(daily_menu_id=daily.id, active=True).order_by(FoodPlate.name).all()
    def create_week(self, week_start_date, label='', active=True):
        if isinstance(week_start_date, str): week_start_date = date.fromisoformat(week_start_date)
        week_start_date = week_start_for(week_start_date)
        week = self.session.query(WeeklyMenu).filter_by(week_start_date=week_start_date).first() or WeeklyMenu(week_start_date=week_start_date)
        week.label = label or f'Semaine {week_start_date.isoformat()}'; week.active = active; self.session.add(week); self.session.flush()
        for offset in range(7):
            service_date = week_start_date + timedelta(days=offset)
            if not self.session.query(DailyMenu).filter_by(weekly_menu_id=week.id, service_date=service_date).first():
                self.session.add(DailyMenu(weekly_menu_id=week.id, service_date=service_date, weekday=offset, active=offset < 5))
        return week
    def add_plate(self, daily_menu_id, name, description='', variants=None):
        if not (name or '').strip(): raise ValueError('error.required')
        plate = FoodPlate(daily_menu_id=daily_menu_id, name=name.strip(), description=description, active=True)
        self.session.add(plate); self.session.flush()
        for size_key, label, price in (variants or DEFAULT_VARIANTS):
            self.session.add(FoodPlateVariant(food_plate_id=plate.id, size_key=size_key, label=label, price=normalize_money(price), active=True))
        return plate
    def copy_previous_week(self, target_week_start):
        if isinstance(target_week_start, str): target_week_start = date.fromisoformat(target_week_start)
        target = self.create_week(target_week_start)
        source = self.session.query(WeeklyMenu).filter(WeeklyMenu.week_start_date < target.week_start_date).order_by(WeeklyMenu.week_start_date.desc()).first()
        if not source: return target
        for source_day in source.days:
            target_day = next(d for d in target.days if d.weekday == source_day.weekday)
            for plate in source_day.plates:
                new_plate = self.add_plate(target_day.id, plate.name, plate.description, [])
                for variant in plate.variants:
                    self.session.add(FoodPlateVariant(food_plate_id=new_plate.id, size_key=variant.size_key, label=variant.label, price=variant.price, active=variant.active))
        return target
    def save_menu(self, weekday, name, price, is_active=True):
        weekday=parse_required_int(weekday); name=(name or '').strip()
        if weekday < 0 or weekday > 6: raise ValueError('Invalid weekday.')
        if not name: raise ValueError('Menu name is required.')
        menu=self.repo.menu_for_weekday(weekday) or LunchMenu(weekday=weekday)
        menu.name=name; menu.price=normalize_money(price); menu.is_active=is_active
        if menu.price < 0: raise ValueError('Price cannot be negative.')
        self.repo.save_menu(menu); return menu
    def charge_today(self, client_id, plate_id=None, variant_id=None, service_date=None, user_id=None):
        service_date=service_date or date.today()
        if plate_id is not None or variant_id is not None:
            plate_id=parse_required_int(plate_id); variant_id=parse_required_int(variant_id)
            plate=self.session.get(FoodPlate, plate_id); variant=self.session.get(FoodPlateVariant, variant_id)
            if not plate or not plate.active or not variant or not variant.active or variant.food_plate_id != plate.id: raise ValueError('error.required')
            order=LunchOrder(client_id=client_id, food_plate_id=plate.id, variant_id=variant.id, service_date=service_date, menu_name=plate.name, plate_name_snapshot=plate.name, variant_label_snapshot=variant.size_key or variant.label, amount=variant.price, created_by_user_id=user_id)
        else:
            menu=self.repo.menu_for_weekday(service_date.weekday())
            if not menu or not menu.is_active: raise ValueError('lunch.no_menu_today')
            order=LunchOrder(client_id=client_id, menu=menu, service_date=service_date, menu_name=menu.name, plate_name_snapshot=menu.name, variant_label_snapshot='', amount=menu.price, created_by_user_id=user_id)
        self.repo.save_order(order); self.session.flush()
        LedgerService(self.session).post_entry(client_id=client_id, entry_type=LEDGER_DEBIT, amount=order.amount, reference_type=REFERENCE_LUNCH, reference_id=order.id, description=f'Lunch: {order.plate_name_snapshot}', created_by_user_id=user_id)
        return order
