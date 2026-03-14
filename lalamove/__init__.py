from typing import Optional
from lalamove.client import APIClient
from lalamove.quotations import Quotation
from lalamove.orders import Order
from lalamove.webhook import Webhook
from lalamove.drivers import Driver


class LalamoveSDK:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        market: str,
        sandbox: Optional[bool] = False,
    ):
        self.client = APIClient(api_key, api_secret, market, sandbox)
        self.quotation = Quotation(self.client)
        self.order = Order(self.client)
        self.webhook = Webhook(self.client)

__all__ = [
    "LalamoveSDK",
    "Quotation",
    "Order",
    "Webhook",
    "Driver",
]

