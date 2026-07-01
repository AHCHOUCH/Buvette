import tempfile
import unittest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING=True; WTF_CSRF_ENABLED=False; SQLALCHEMY_DATABASE_URI='sqlite:///' + tempfile.NamedTemporaryFile(delete=True).name

class ProductionHardeningTests(unittest.TestCase):
    def setUp(self): self.app=create_app(TestConfig); self.client=self.app.test_client()
    def login(self, username='administrator', password='administrator'):
        return self.client.post('/auth/login', data={'username':username,'password':password})
    def test_login_roles_permissions_and_languages(self):
        self.assertEqual(self.login('cashier','cashier').status_code,302)
        self.assertEqual(self.client.get('/settings/').status_code,403)
        self.assertIn('dir="rtl"'.encode(), self.client.get('/dashboard/').data)
        self.client.post('/auth/logout')
        self.login('administrator','administrator')
        self.assertEqual(self.client.get('/settings/').status_code,200)
        self.assertIn('dir="ltr"'.encode(), self.client.get('/dashboard/').data)
    def test_user_creation_audit_and_logs(self):
        self.login()
        r=self.client.post('/users/', data={'username':'second','password':'secret123','full_name':'Second User','role':'cashier','active':'y'}, follow_redirects=True)
        self.assertEqual(r.status_code,200); self.assertIn(b'second', r.data)
        self.assertIn(b'user.create', self.client.get('/logs/').data)
    def test_client_employee_number_and_financial_ledger(self):
        self.login()
        self.client.post('/clients/new', data={'name':'Bob Staff','debt_limit':'5','is_active':'y'}, follow_redirects=True)
        with self.app.app_context():
            from app.models import BreakfastProduct, Client
            c=Client.query.filter_by(name='Bob Staff').first(); self.assertTrue(c.account_code.startswith('EMP-'))
            product_id=BreakfastProduct.query.first().id; cid=c.id
        self.assertEqual(self.client.post('/breakfast/', data={'client_id':cid, f'qty_{product_id}':'2'}, follow_redirects=True).status_code,200)
        self.assertEqual(self.client.post('/lunch/', data={'client_id':cid}, follow_redirects=True).status_code,200)
        self.assertEqual(self.client.post('/payments/', data={'client_id':cid,'amount':'2.00'}, follow_redirects=True).status_code,200)
        data=self.client.get('/ledger/').data
        self.assertIn(b'Breakfast', data); self.assertIn(b'Cash payment', data)
    def test_supplier_charges_do_not_touch_client_balance_and_delete_blocked(self):
        self.login()
        with self.app.app_context():
            from app.models import Client, Supplier
            cid=Client.query.first().id; supplier=Supplier.query.first(); sid=supplier.id
            before=sum([e.amount if e.entry_type=='debit' else -e.amount for e in Client.query.get(cid).ledger_entries])
        r=self.client.post('/charges/', data={'supplier_id':sid,'amount':'3.00','category':'Other'}, follow_redirects=True)
        self.assertEqual(r.status_code,200)
        with self.app.app_context():
            from app.models import Client
            after=sum([e.amount if e.entry_type=='debit' else -e.amount for e in Client.query.get(cid).ledger_entries])
            self.assertEqual(before, after)
        blocked=self.client.post(f'/charges/suppliers/{sid}/delete', data={'password':'administrator'}, follow_redirects=True)
        self.assertIn(b'Cannot delete supplier with financial history', blocked.data)

if __name__=='__main__': unittest.main()
