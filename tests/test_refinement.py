import unittest
from datetime import date
from app import create_app, db
from app.i18n.translations import TRANSLATIONS
from app.lunch.service import LunchService
from app.models import Client, LedgerEntry, LunchOrder, ManualCharge, Supplier

class RefinementTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app(); self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.ctx=self.app.app_context(); self.ctx.push(); db.drop_all(); db.create_all()
        from app import _seed_data
        _seed_data(); self.client=self.app.test_client()
    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()
    def login(self, username='administrator', password='administrator'):
        return self.client.post('/auth/login', data={'username':username,'password':password}, follow_redirects=True)
    def test_weekdays_buttons_and_role_direction(self):
        self.assertEqual(TRANSLATIONS['fr']['weekday.monday'], 'Lundi')
        self.assertEqual(TRANSLATIONS['ar']['weekday.monday'], 'الإثنين')
        self.assertEqual(TRANSLATIONS['fr']['button.save'], 'Enregistrer')
        self.login('cashier','cashier')
        page=self.client.get('/dashboard/').data.decode()
        self.assertIn('lang="ar"', page); self.assertIn('dir="rtl"', page); self.assertIn('العمليات', page)
    def test_weekly_menu_order_snapshot_and_price(self):
        self.login()
        svc=LunchService(db.session); week=svc.create_week(date(2026,7,6), 'Test'); db.session.flush()
        plate=svc.add_plate(week.days[0].id, 'Tajine'); db.session.flush()
        client=Client.query.first(); variant=plate.variants[1]
        order=svc.charge_today(client.id, plate.id, variant.id, service_date=date(2026,7,6), user_id=1); db.session.commit()
        self.assertEqual(order.amount, variant.price); self.assertEqual(order.plate_name_snapshot, 'Tajine')
        self.assertEqual(LedgerEntry.query.filter_by(reference_id=order.id).count(), 1)
    def test_supplier_expense_not_client_ledger(self):
        client=Client.query.first(); supplier=Supplier.query.first()
        before=LedgerEntry.query.filter_by(client_id=client.id).count()
        db.session.add(ManualCharge(supplier_id=supplier.id, amount='30.00', category='Cleaning'))
        db.session.commit()
        self.assertEqual(LedgerEntry.query.filter_by(client_id=client.id).count(), before)

if __name__ == '__main__':
    unittest.main()
