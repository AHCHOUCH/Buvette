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
    def test_navigation_groups_render_as_adjacent_dropdowns(self):
        self.login()
        page=self.client.get('/dashboard/').data.decode()
        self.assertIn('<nav class="app-navigation"', page)
        self.assertEqual(page.count('<details class="nav-dropdown"'), 4)
        self.assertIn('<div class="nav-dropdown-menu">', page)
        self.assertNotIn('<aside class="app-sidebar"', page)
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

class ClosureRegressionTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app(); self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.ctx=self.app.app_context(); self.ctx.push(); db.drop_all(); db.create_all()
        from app import _seed_data
        _seed_data(); self.client=self.app.test_client()
    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()
    def login(self, username='administrator', password='administrator'):
        return self.client.post('/auth/login', data={'username':username,'password':password}, follow_redirects=True)
    def test_lunch_order_without_legacy_menu_id_succeeds(self):
        svc=LunchService(db.session); week=svc.create_week(date(2026,7,6), 'Semaine test'); db.session.flush()
        plate=svc.add_plate(week.days[0].id, 'Couscous'); db.session.flush()
        client=Client.query.first(); variant=plate.variants[0]
        order=svc.charge_today(client.id, plate.id, variant.id, service_date=date(2026,7,6), user_id=1); db.session.commit()
        self.assertIsNone(order.menu_id)
        self.assertEqual(LunchOrder.query.count(), 1)
    def test_empty_lunch_dropdowns_show_validation_not_traceback(self):
        self.login('cashier','cashier')
        response=self.client.post('/lunch/', data={'client_id':'','plate_id':'','variant_id':''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('هذا الحقل ضروري'.encode(), response.data)
    def test_invalid_lunch_numeric_ids_show_validation(self):
        self.login('cashier','cashier')
        response=self.client.post('/lunch/', data={'client_id':'abc','plate_id':'x','variant_id':'y'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('هذا الحقل ضروري'.encode(), response.data)
    def test_variant_price_edit_preserves_order_snapshot_amount(self):
        svc=LunchService(db.session); week=svc.create_week(date(2026,7,6), 'Semaine test'); db.session.flush()
        plate=svc.add_plate(week.days[0].id, 'Pastilla'); db.session.flush()
        client=Client.query.first(); variant=plate.variants[0]
        order=svc.charge_today(client.id, plate.id, variant.id, service_date=date(2026,7,6), user_id=1); old_amount=order.amount
        variant.price='99.00'; db.session.commit()
        self.assertEqual(LunchOrder.query.get(order.id).amount, old_amount)
    def test_numeric_keypad_function_is_exported(self):
        js=open('app/static/js/app.js', encoding='utf-8').read()
        self.assertIn("key === '.'", js)
        self.assertIn("'0.'", js)
        self.assertIn('applyNumericKey', js)

if __name__ == '__main__':
    unittest.main()

class UrgentBugfixTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app(); self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.ctx=self.app.app_context(); self.ctx.push(); db.drop_all(); db.create_all()
        from app import _seed_data
        _seed_data(); self.client=self.app.test_client()
    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()
    def login(self, username='administrator', password='administrator'):
        return self.client.post('/auth/login', data={'username':username,'password':password}, follow_redirects=True)
    def test_cashier_dashboard_200_arabic_not_unauthorized(self):
        self.login('cashier','cashier')
        response=self.client.get('/dashboard/')
        body=response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('لوحة التحكم', body)
        self.assertNotIn('غير مسموح', body)
    def test_lunch_forced_db_error_hides_sql_text(self):
        from unittest.mock import patch
        self.login('cashier','cashier')
        with patch('app.lunch.service.LunchService.charge_today', side_effect=Exception('sqlite IntegrityError SQL INSERT INTO lunch_orders sqlalche.me')):
            response=self.client.post('/lunch/', data={'client_id':'1','plate_id':'1','variant_id':'1'}, follow_redirects=True)
        body=response.data.decode()
        self.assertIn('حدث خطأ', body)
        for forbidden in ('sqlite','IntegrityError','SQL','sqlalche.me','INSERT INTO'):
            self.assertNotIn(forbidden, body)
    def test_weekend_lunch_closed_message(self):
        from unittest.mock import patch
        self.login('cashier','cashier')
        with patch('app.lunch.routes.date') as fake_date:
            fake_date.today.return_value=date(2026,7,4)
            fake_date.side_effect=lambda *a, **k: date(*a, **k)
            response=self.client.get('/lunch/')
        self.assertIn('البوفيت مغلق اليوم'.encode(), response.data)
    def test_no_menu_warning_message(self):
        self.login('cashier','cashier')
        response=self.client.get('/lunch/')
        self.assertIn('لا توجد قائمة نشطة لهذا اليوم'.encode(), response.data)
    def test_variant_labels_by_role_language(self):
        svc=LunchService(db.session); week=svc.create_week(date.today(), 'Current'); db.session.flush()
        svc.add_plate(week.days[date.today().weekday()].id, 'Plat'); db.session.commit()
        self.login('cashier','cashier')
        ar=self.client.get('/lunch/').data.decode()
        self.assertIn('صغير — 20 DH', ar)
        self.client.post('/auth/logout', follow_redirects=True)
        self.login('administrator','administrator')
        fr=self.client.get('/lunch/').data.decode()
        self.assertIn('Petit — 20 DH', fr)

class IdentitySettingsLedgerExportTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app(); self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.ctx=self.app.app_context(); self.ctx.push(); db.drop_all(); db.create_all()
        from app import _seed_data
        _seed_data(); self.client=self.app.test_client()
    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()
    def login(self, username='administrator', password='administrator'):
        return self.client.post('/auth/login', data={'username':username,'password':password}, follow_redirects=True)
    def _make_entry(self, day):
        from datetime import datetime
        client=Client.query.first()
        db.session.add(LedgerEntry(client_id=client.id, entry_type='debit', amount='7.00', running_balance='7.00', reference_type='breakfast', reference_id=day.day, description=f'Breakfast {day}', timestamp=datetime(day.year, day.month, day.day, 9, 0), created_by_user_id=1))
        db.session.commit()
    def test_login_hides_debug_credentials_and_uses_identity(self):
        page=self.client.get('/auth/login').data.decode()
        self.assertNotIn('DEBUG: administrator / administrator', page)
        self.assertIn('Buvette Manager', page)
        self.assertIn('Nom d’utilisateur', page)
    def test_settings_identity_updates_title_header_and_colors(self):
        self.login()
        r=self.client.post('/settings/', data={'organization_name':'Buvette Test','organization_short_name':'bt','currency':'DH','footer_text':'Pied','debt_warning_default':'50','primary_color':'#123456','secondary_color':'#eeeeee','accent_color':'#abcdef','header_background_color':'#234567','sidebar_background_color':'#f0f0f0','button_color':'#345678','login_background_color':'#fafafa'}, follow_redirects=True)
        body=r.data.decode(); self.assertIn('Paramètres enregistrés', body)
        dash=self.client.get('/dashboard/').data.decode()
        self.assertIn('Buvette Test', dash); self.assertIn('--header-bg:#234567', dash)
    def test_admin_can_export_complete_and_empty_ledger_headers_and_audit(self):
        self.login(); r=self.client.get('/ledger/export.csv?scope=all')
        body=r.data.decode('utf-8-sig')
        self.assertEqual(r.status_code, 200)
        self.assertIn('date,client employee number,client name,transaction type,description,debit,credit,running balance,created by,reference/order id', body)
        from app.models import AuditLog
        self.assertEqual(AuditLog.query.filter_by(action='ledger.export').count(), 1)
    def test_admin_filtered_export_respects_date_filters(self):
        from datetime import date
        self._make_entry(date(2026,7,1)); self._make_entry(date(2026,8,1)); self.login()
        body=self.client.get('/ledger/export.csv?start_date=2026-07-01&end_date=2026-07-31').data.decode('utf-8-sig')
        self.assertIn('Breakfast 2026-07-01', body); self.assertNotIn('Breakfast 2026-08-01', body)
    def test_cashier_cannot_export_ledger_without_permission(self):
        self.login('cashier','cashier')
        self.assertEqual(self.client.get('/ledger/export.csv?scope=all').status_code, 403)
