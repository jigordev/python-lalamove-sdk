import pytest
import httpx
from httpx import Response, Request, MockTransport
from lalamove import LalamoveSDK
from lalamove.enums import Language
from lalamove.quotations import QuotationData, QuotationStop, QuotationCoord
from lalamove.orders import OrderData, OrderSender, OrderDeliveryDetails, OrderStop, OrderUpdateData, OrderCoord


def get_sdk_with_mock(handler):
    transport = MockTransport(handler)
    sdk = LalamoveSDK("dummy_key", "dummy_secret", "BR", sandbox=True)
    sdk.client.http = httpx.Client(transport=transport)
    return sdk


def test_quotation_create():
    def handler(request: Request) -> Response:
        assert request.method == "POST"
        assert request.url.path == "/v3/quotations"
        data = {
            "data": {
                "quotationId": "1514140994227007571",
                "scheduleAt": "2022-04-13T07:18:38.00Z",
                "expiresAt": "2022-04-13T07:23:39.00Z",
                "serviceType": "MOTORCYCLE",
                "specialRequests": ["TOLL_FEE_10"],
                "language": "pt_BR",
                "stops": [
                    {
                        "stopId": "1514140995971838016",
                        "coordinates": {"lat": "22.3354735", "lng": "114.1761581"},
                        "address": "Innocentre, 72 Tat Chee Ave, Kowloon Tong"
                    }
                ],
                "isRouteOptimized": False,
                "priceBreakdown": {
                    "base": "90",
                    "specialRequests": "13",
                    "vat": "21",
                    "totalBeforeOptimization": "124",
                    "totalExcludePriorityFee": "124",
                    "total": "124",
                    "currency": "BRL"
                },
                "item": {
                    "quantity": "1",
                    "weight": "LESS_THAN_3_KG",
                    "categories": ["OFFICE_ITEM"],
                    "handlingInstructions": []
                }
            }
        }
        return Response(201, json=data)

    sdk = get_sdk_with_mock(handler)
    data = QuotationData(
        service_type="MOTORCYCLE",
        stops=[
            QuotationStop(coordinates=QuotationCoord(lat="22.3354735", lng="114.1761581"), address="Innocentre")
        ],
        language=Language.PT_BR
    )
    result = sdk.quotation.create(data)
    assert result.data.quotation_id == "1514140994227007571"
    assert result.data.price_breakdown.total == "124"


def test_quotation_get_details():
    def handler(request: Request) -> Response:
        assert request.method == "GET"
        assert request.url.path == "/v3/quotations/1514140994227007571"
        data = {
            "data": {
                "quotationId": "1514140994227007571",
                "scheduleAt": "2022-04-13T07:18:38.00Z",
                "expiresAt": "2022-04-13T07:23:39.00Z",
                "serviceType": "MOTORCYCLE",
                "specialRequests": ["TOLL_FEE_10"],
                "language": "pt_BR",
                "stops": [],
                "isRouteOptimized": False,
                "priceBreakdown": {
                    "base": "90",
                    "specialRequests": "13",
                    "vat": "21",
                    "totalBeforeOptimization": "124",
                    "totalExcludePriorityFee": "124",
                    "total": "124",
                    "currency": "BRL"
                },
                "item": {
                    "quantity": "1",
                    "weight": "LESS_THAN_3_KG",
                    "categories": ["OFFICE_ITEM"],
                    "handlingInstructions": []
                }
            }
        }
        return Response(200, json=data)

    sdk = get_sdk_with_mock(handler)
    result = sdk.quotation.get_details("1514140994227007571")
    assert result.data.quotation_id == "1514140994227007571"


def test_order_place():
    def handler(request: Request) -> Response:
        assert request.method == "POST"
        assert request.url.path == "/v3/orders"
        data = {
            "data": {
                "orderId": "1000000000",
                "quotationId": "1514140994227007571",
                "priceBreakDown": {
                    "base": "90",
                    "extraMileage": "0",
                    "surcharge": "0",
                    "totalExcludePriorityFee": "90",
                    "total": "90",
                    "currency": "BRL",
                    "priorityFee": "0"
                },
                "driverId": "12345",
                "shareLink": "https://lalamove.com/share/1000000000",
                "status": "ASSIGNING_DRIVER",
                "distance": {"value": "5000", "unit": "m"},
                "stops": [
                    {
                        "coordinates": {"lat": "22.335", "lng": "114.17"},
                        "address": "Innocentre",
                        "name": "Jane Doe",
                        "phone": "+5511999999999",
                        "pod": None
                    }
                ],
                "metadata": {}
            }
        }
        return Response(201, json=data)

    sdk = get_sdk_with_mock(handler)
    data = OrderData(
        quotation_id="1514140994227007571",
        sender=OrderSender(stop_id="112345623", name="John Doe", phone="+5511888888888"),
        recipients=[
            OrderDeliveryDetails(stop_id="1514140995971838016", name="Jane Doe", phone="+5511999999999", remarks="Leave at door")
        ]
    )
    result = sdk.order.place(data)
    assert result.data.order_id == "1000000000"
    assert result.data.status == "ASSIGNING_DRIVER"


def test_order_get_details():
    def handler(request: Request) -> Response:
        assert request.method == "GET"
        assert request.url.path == "/v3/orders/1000000000"
        data = {
            "data": {
                "orderId": "1000000000",
                "quotationId": "1514140994227007571",
                "priceBreakDown": {
                    "base": "90",
                    "extraMileage": "0",
                    "surcharge": "0",
                    "totalExcludePriorityFee": "90",
                    "total": "90",
                    "currency": "BRL",
                    "priorityFee": "0"
                },
                "driverId": "12345",
                "shareLink": "https://lalamove.com/share/1000000000",
                "status": "ON_GOING",
                "distance": {"value": "5000", "unit": "m"},
                "stops": [],
                "metadata": {}
            }
        }
        return Response(200, json=data)

    sdk = get_sdk_with_mock(handler)
    result = sdk.order.get_details("1000000000")
    assert result.data.order_id == "1000000000"
    assert result.data.status == "ON_GOING"


def test_order_add_priority_fee():
    def handler(request: Request) -> Response:
        assert request.method == "POST"
        assert request.url.path == "/v3/orders/1000000000/priority-fee"
        data = {
            "data": {
                "orderId": "1000000000",
                "quotationId": "1514140994227007571",
                "priceBreakDown": {
                    "base": "90",
                    "extraMileage": "0",
                    "surcharge": "0",
                    "totalExcludePriorityFee": "90",
                    "total": "100",
                    "currency": "BRL",
                    "priorityFee": "10"
                },
                "driverId": "12345",
                "shareLink": "https://lalamove.com/share/1000000000",
                "status": "ASSIGNING_DRIVER",
                "distance": {"value": "5000", "unit": "m"},
                "stops": [],
                "metadata": {}
            }
        }
        return Response(201, json=data)

    sdk = get_sdk_with_mock(handler)
    result = sdk.order.add_priority_fee("1000000000", "10")
    assert result.data.price_break_down.total == "100"


def test_order_edit():
    def handler(request: Request) -> Response:
        assert request.method == "PATCH"
        assert request.url.path == "/v3/orders/1000000000"
        data = {
            "data": {
                "orderId": "1000000000",
                "quotationId": "1514140994227007571",
                "priceBreakDown": {
                    "base": "90",
                    "extraMileage": "0",
                    "surcharge": "0",
                    "totalExcludePriorityFee": "90",
                    "total": "90",
                    "currency": "BRL",
                    "priorityFee": "0"
                },
                "driverId": "12345",
                "shareLink": "https://lalamove.com/share/1000000000",
                "status": "ASSIGNING_DRIVER",
                "distance": {"value": "5000", "unit": "m"},
                "stops": [],
                "metadata": {}
            }
        }
        return Response(200, json=data)

    sdk = get_sdk_with_mock(handler)
    update_data = OrderUpdateData(
        stops=[
            OrderStop(
                coordinates=OrderCoord(lat="22.335", lng="114.17"),
                address="Innocentre",
                name="Jane Doe",
                phone="+5511999999999"
            )
        ]
    )
    result = sdk.order.edit("1000000000", update_data)
    assert result.data.order_id == "1000000000"


def test_order_cancel():
    def handler(request: Request) -> Response:
        assert request.method == "DELETE"
        assert request.url.path == "/v3/orders/1000000000"
        return Response(204)

    sdk = get_sdk_with_mock(handler)
    sdk.order.cancel("1000000000")


def test_driver_get_details():
    def handler(request: Request) -> Response:
        assert request.method == "GET"
        assert request.url.path == "/v3/orders/1000000000/drivers/12345"
        data = {
            "data": {
                "driverId": "12345",
                "name": "Driver Name",
                "phone": "+5511777777777",
                "plateNumber": "ABC-1234",
                "photo": "https://example.com/photo.jpg",
                "coordinates": {
                    "lat": "22.335",
                    "lng": "114.17",
                    "updatedAt": "2023-01-01T00:00:00Z"
                }
            }
        }
        return Response(200, json=data)

    sdk = get_sdk_with_mock(handler)
    result = sdk.order.driver.get_details("1000000000", "12345")
    assert result.data.driver_id == "12345"
    assert result.data.name == "Driver Name"


def test_driver_change():
    def handler(request: Request) -> Response:
        assert request.method == "DELETE"
        assert request.url.path == "/v3/orders/1000000000/drivers/12345"
        return Response(204)

    sdk = get_sdk_with_mock(handler)
    sdk.order.driver.change("1000000000", "12345")


def test_webhook_set():
    def handler(request: Request) -> Response:
        assert request.method == "PATCH"
        assert request.url.path == "/v3/webhook"
        data = {
            "data": {
                "url": "https://example.com/webhook"
            }
        }
        return Response(200, json=data)

    sdk = get_sdk_with_mock(handler)
    result = sdk.webhook.set_webhook("https://example.com/webhook")
    assert result.data.url == "https://example.com/webhook"
