"""Regression checks for the touch-first shell and cashier controls."""
import tempfile
import unittest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + tempfile.NamedTemporaryFile(delete=True).name


class TouchInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def login(self, username, password):
        return self.client.post("/auth/login", data={"username": username, "password": password})

    def test_shell_uses_top_navigation_and_page_scroll_buttons(self):
        self.login("cashier", "cashier")
        page = self.client.get("/dashboard/").data
        self.assertIn(b"app-topnav", page)
        self.assertNotIn(b"<aside", page)
        self.assertIn(b'data-scroll-page="up"', page)
        self.assertIn(b'data-scroll-page="down"', page)

    def test_cashier_amounts_and_quantities_are_button_controlled(self):
        self.login("cashier", "cashier")
        for path in ("/breakfast/", "/payments/", "/charges/"):
            page = self.client.get(path).data
            self.assertIn(b"button-controlled-input", page)
            self.assertIn(b"readonly", page)
            self.assertIn(b'inputmode="none"', page)

    def test_both_dashboard_modes_use_touch_dashboard_cards(self):
        self.login("cashier", "cashier")
        self.assertIn(b"cashier-metrics", self.client.get("/dashboard/").data)
        self.client.post("/auth/logout")
        self.login("administrator", "administrator")
        page = self.client.get("/dashboard/").data
        self.assertIn(b"admin-metrics", page)
        self.assertIn(b"dashboard-period", page)


if __name__ == "__main__":
    unittest.main()
