import httpx
from lalamove.client import APIClient
from httpx import Response, Request, MockTransport


def test_post_quotation_with_mock():
    def handler(request: Request) -> Response:
        data = {
            "data": {
                "quotationId": "1514140994227007571",
                "scheduleAt": "2022-04-13T07:18:38.00Z",
                "expiresAt": "2022-04-13T07:23:39.00Z",
                "serviceType": "MOTORCYCLE",
                "specialRequests": ["TOLL_FEE_10", "PURCHASE_SERVICE_1"],
                "language": "EN_HK",
                "stops": [
                    {
                        "stopId": "1514140995971838016",
                        "coordinates": {"lat": "22.3354735", "lng": "114.1761581"},
                        "address": "Innocentre, 72 Tat Chee Ave, Kowloon Tong",
                    },
                    {
                        "stopId": "1514140995971838017",
                        "coordinates": {"lat": "22.2812946", "lng": "114.1598610"},
                        "address": "Statue Square, Des Voeux Rd Central, Central",
                    },
                ],
                "isRouteOptimized": False,
                "priceBreakdown": {
                    "base": "90",
                    "specialRequests": "13",
                    "vat": "21",
                    "totalBeforeOptimization": "124",
                    "totalExcludePriorityFee": "124",
                    "total": "124",
                    "currency": "HKD",
                },
                "item": {
                    "weight": "LESS_THAN_3_KG",
                    "categories": ["OFFICE_ITEM", "OTHERS"],
                },
                "distance": {"value": "5836", "unit": "m"},
            }
        }

        assert request.method == "POST"
        assert request.url.path == "/v3/quotations"
        assert request.headers["Authorization"].startswith("hmac ")
        return Response(200, json=data)

    transport = MockTransport(handler)
    client = APIClient("dummy_key", "dummy_secret", "BR", sandbox=True)
    client.http = httpx.Client(transport=transport)

    data = {
        "data": {
            "scheduleAt": "2020-09-01T14:30:00.00Z",
            "serviceType": "MOTORCYCLE",
            "specialRequests": ["TOLL_FEE_10", "PURCHASE_SERVICE_1"],
            "language": "en_HK",
            "stops": [
                {
                    "coordinates": {"lat": "22.3353139", "lng": "114.1758402"},
                    "address": "Jl. Perum Dasana",
                },
                {
                    "coordinates": {"lat": "22.2812946", "lng": "114.1598610"},
                    "address": "Statue Square, Des Voeux Rd Central, Central",
                },
            ],
            "item": {
                "quantity": "3",
                "weight": "LESS_THAN_3KG",
                "categories": ["FOOD_DELIVERY", "OFFICE_ITEM"],
                "handlingInstructions": ["KEEP_UPRIGHT"],
            },
            "isRouteOptimized": True,
        }
    }

    quotation = client.make_request(
        "POST",
        "quotations",
        data=data,
    )

    assert quotation["data"]["priceBreakdown"]["total"] == "124"
