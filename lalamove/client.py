import httpx
import json
import uuid
from typing import Optional, Dict
from lalamove.auth import HttpMethod, get_auth_token
from lalamove.enums import Market
from lalamove.utils import convert_keys_to_camel_case
from lalamove.errors import (
    BadRequest,
    Unauthorized,
    PaymentRequired,
    Forbidden,
    NotFound,
    UnprocessableEntity,
    InsufficientStops,
    OrderNotFound,
    InvalidField,
    MissingField,
    TooManyStops,
    InvalidQuotationID,
    TooManyRequests,
    InternalServerError,
)

DEV_BASE_URL = "https://rest.sandbox.lalamove.com/v3"
PROD_BASE_URL = "https://rest.lalamove.com/v3"


class APIClient:
    def __init__(
        self, api_key: str, api_secret: str, market: Market, sandbox: bool = False, timeout: float = 30.0
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox
        self.market = market
        self.base_url = DEV_BASE_URL if sandbox else PROD_BASE_URL
        self.http = httpx.Client(timeout=timeout)

    def _make_request(self, method: HttpMethod, endpoint: str, data: Optional[Dict] = None):
        data = convert_keys_to_camel_case(data)
        body = json.dumps(data) if data else ""

        token = get_auth_token(
            self.api_key,
            self.api_secret,
            method.upper(),
            endpoint,
            body,
        )

        headers = {
            "Authorization": f"hmac {token}",
            "Market": self.market,
            "Request-ID": str(uuid.uuid4()),
        }

        url = f"{self.base_url}/{endpoint}"

        return self.http.request(method, url, headers=headers, json=data)

    def make_request(self, method: HttpMethod, endpoint: str, data: Optional[Dict] = None):
        try:
            response = self._make_request(method, endpoint, data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            error_data = error.response.json()
            message = error_data.get("message")

            match error.response.status_code:
                case 400:
                    raise BadRequest(
                        "Bad Request", request=error.request, response=error.response
                    )
                case 401:
                    raise Unauthorized(
                        "Unauthorized", request=error.request, response=error.response
                    )
                case 402:
                    raise PaymentRequired(
                        "Payment Required",
                        request=error.request,
                        response=error.response,
                    )
                case 403:
                    raise Forbidden(
                        "Forbidden", request=error.request, response=error.response
                    )
                case 404:
                    raise NotFound(
                        "Not Found", request=error.request, response=error.response
                    )
                case 422:
                    match message:
                        case "ERR_INSUFFICIENT_STOPS":
                            raise InsufficientStops(
                                message, request=error.request, response=error.response
                            )
                        case "ERR_ORDER_NOT_FOUND":
                            raise OrderNotFound(
                                message, request=error.request, response=error.response
                            )
                        case "ERR_INVALID_FIELD":
                            raise InvalidField(
                                message, request=error.request, response=error.response
                            )
                        case "ERR_MISSING_FIELD":
                            raise MissingField(
                                message, request=error.request, response=error.response
                            )
                        case "ERR_TOO_MANY_STOPS":
                            raise TooManyStops(
                                message, request=error.request, response=error.response
                            )
                        case "ERR_INVALID_QUOTATION_ID":
                            raise InvalidQuotationID(
                                message, request=error.request, response=error.response
                            )
                        case _:
                            raise UnprocessableEntity(
                                message, request=error.request, response=error.response
                            )
                case 429:
                    raise TooManyRequests(
                        "Too Many Requests",
                        request=error.request,
                        response=error.response,
                    )
                case 500:
                    raise InternalServerError(
                        "Internal Server Error",
                        request=error.request,
                        response=error.response,
                    )
                case _:
                    raise error
