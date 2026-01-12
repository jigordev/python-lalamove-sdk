from lalamove.client import APIClient
from lalamove.drivers import Driver
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel


class OrderSender(BaseModel):
    name: str
    phone: str


class OrderDeliveryDetails(BaseModel):
    stop_id: str
    name: str
    phone: str
    remarks: str


class OrderData(BaseModel):
    quotation_id: str
    sender: OrderSender
    recipients: List[OrderDeliveryDetails]
    is_pod_enabled: Optional[bool] = False
    partner: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class OrderBody(BaseModel):
    data: OrderData


class OrderPriceBreakdown(BaseModel):
    base: str
    extra_mileage: str
    surcharge: str
    total_exclude_priority_fee: str
    total: str
    currency: str
    priority_fee: str


class OrderDistance(BaseModel):
    value: str
    unit: str


class OrderCoord(BaseModel):
    lat: str
    lng: str


class OrderPOD(BaseModel):
    status: str
    image: str
    delivered_at: datetime


class OrderStop(BaseModel):
    coordinates: OrderCoord
    address: str
    name: str
    phone: str
    pod: Optional[OrderPOD]


class OrderResponseData(BaseModel):
    order_id: str
    quotation_id: str
    price_break_down: OrderPriceBreakdown
    driver_id: str
    share_link: str
    status: str
    distance: OrderDistance
    stops: List[OrderStop]
    metadata: Dict


class OrderResponse(BaseModel):
    data: OrderResponseData


class OrderPriorityFeeData(BaseModel):
    priority_fee: str


class OrderPriorityFeeBody(BaseModel):
    data: OrderPriorityFeeData


class OrderUpdateData(BaseModel):
    stops: List[OrderStop]


class OrderUpdateBody(BaseModel):
    data: OrderUpdateData


class Order:
    def __init__(self, client: APIClient):
        self.client = client
        self.driver = Driver(client)

    def place(self, data: OrderData) -> OrderResponse:
        data = OrderBody(data=data)
        response = self.client.make_request("POST", "orders", data.model_dump())
        return OrderResponse.model_validate({"data": response})

    def get_details(self, order_id: str) -> OrderResponse:
        response = self.client.make_request("GET", f"orders/{order_id}")
        return OrderResponse.model_validate({"data": response})

    def add_priority_fee(self, order_id: str, priority_fee: str) -> OrderResponse:
        data = OrderPriorityFeeBody(
            data=OrderPriorityFeeData(priority_fee=priority_fee)
        )
        response = self.client.make_request(
            "POST", f"orders/{order_id}/priority-fee", data.model_dump()
        )
        return OrderResponse.model_validate({"data": response})

    def edit(self, order_id: str, data: OrderUpdateData) -> OrderResponse:
        data = OrderUpdateBody(data=data)
        response = self.client.make_request("PATCH", f"orders/{order_id}", data.model_dump())
        return OrderResponse.model_validate({"data": response})

    def cancel(self, order_id: str) -> None:
        self.client.make_request("DELETE", f"orders/{order_id}")
