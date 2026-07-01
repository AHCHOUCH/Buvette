import tempfile
import unittest

from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + tempfile.NamedTemporaryFile(delete=True).name


class MvpFlowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def login(self):
        return self.client.post("/auth/login", data={"username": "cashier", "password": "cashier"})

    def test_authentication_and_dashboard(self):
        self.assertEqual(self.client.get("/dashboard/").status_code, 302)
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get("/dashboard/").status_code, 200)
        self.assertEqual(self.client.get("/health").json, {"status": "ok"})

    def test_client_crud_and_search(self):
        self.login()
        response = self.client.post("/clients/new", data={"name": "Alice Staff", "account_code": "A1", "debt_limit": "10", "is_active": "y"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alice Staff", self.client.get("/clients/?q=Alice").data)

    def test_breakfast_lunch_charges_payments_and_ledger(self):
        self.login()
        self.client.post("/clients/new", data={"name": "Bob Staff", "account_code": "B1", "debt_limit": "5", "is_active": "y"}, follow_redirects=True)
        with self.app.app_context():
            from app.models import BreakfastProduct, Client
            client_id = Client.query.filter_by(account_code="B1").first().id
            product_id = BreakfastProduct.query.first().id
        self.assertEqual(self.client.post("/breakfast/", data={"client_id": client_id, f"qty_{product_id}": "2"}, follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post("/lunch/", data={"client_id": client_id}, follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post("/charges/", data={"client_id": client_id, "amount": "3.00", "category": "Miscellaneous"}, follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post("/payments/", data={"client_id": client_id, "amount": "2.00"}, follow_redirects=True).status_code, 200)
        ledger = self.client.get("/ledger/")
        self.assertEqual(ledger.status_code, 200)
        self.assertIn(b"Breakfast", ledger.data)
        self.assertIn(b"Cash payment", ledger.data)

    def test_settings(self):
        self.login()
        response = self.client.post("/settings/", data={"organization_name": "Demo Buvette", "debt_warning_default": "75", "currency": "EUR"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Settings saved", response.data)


if __name__ == "__main__":
    unittest.main()
