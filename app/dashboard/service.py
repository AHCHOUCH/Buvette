"""Dashboard service placeholders for future analytics."""

from decimal import Decimal


class DashboardService:
    """Stable dashboard interface without implementing analytics yet."""

    @staticmethod
    def todays_charges() -> Decimal:
        return Decimal("0.00")

    @staticmethod
    def todays_payments() -> Decimal:
        return Decimal("0.00")

    @staticmethod
    def outstanding_balances() -> Decimal:
        return Decimal("0.00")
