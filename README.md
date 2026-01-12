# Lalamove Python SDK

A simple Python SDK to interact with the [Lalamove API v3](https://developers.lalamove.com/) using a clean and typed interface. This SDK supports operations for quotations, orders, driver management, and webhook registration.

## Features

* Fully typed models using [Pydantic](https://docs.pydantic.dev/)
* Support for Sandbox and Production environments
* Custom exception handling for API errors
* Request signature generation (HMAC)
* Enum support for `Market` and `Language`
* Built-in client for:

  * Quotations
  * Orders (including priority fees, editing, canceling)
  * Drivers (details and reassignment)
  * Webhooks

---

## Installation

```bash
pip install lalamove-sdk
```

---

## Getting Started

### 1. Initialize the SDK

```python
from lalamove import LalamoveSDK
from lalamove.enums import Market

sdk = LalamoveSDK(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    market=Market.BR,
    sandbox=True  # Set to False for production
)
```

---

## Usage

### Quotations

```python
from lalamove.quotations import QuotationData, QuotationStop, QuotationCoord
from lalamove.enums import Language

data = QuotationData(
    service_type="MOTORCYCLE",
    stops=[
        QuotationStop(coordinates=QuotationCoord(lat="12.34", lng="56.78"), address="Start Address"),
        QuotationStop(coordinates=QuotationCoord(lat="23.45", lng="67.89"), address="End Address"),
    ],
    language=Language.EN_BR,
)

quotation = sdk.quotation.create(data)
print(quotation.data.quotation_id)
```

---

### Orders

```python
from lalamove.orders import OrderData, OrderSender, OrderDeliveryDetails

data = OrderData(
    quotation_id="your_quotation_id",
    sender=OrderSender(name="John Doe", phone="+5511999999999"),
    recipients=[
        OrderDeliveryDetails(
            stop_id="stop_id_1",
            name="Jane Doe",
            phone="+5511888888888",
            remarks="Leave at door"
        )
    ]
)

order = sdk.order.place(data)
print(order.data.order_id)
```

#### Cancel an Order

```python
sdk.order.cancel(order_id="your_order_id")
```

---

### Drivers

```python
driver_info = sdk.order.driver.get_details(order_id="your_order_id", driver_id="driver_id")
print(driver_info.data.name)
```

#### Reassign Driver

```python
sdk.order.driver.change(order_id="your_order_id", driver_id="driver_id")
```

---

### Webhooks

```python
from lalamove.webhook import WebhookData

webhook = sdk.webhook.create(WebhookData(url="https://yourdomain.com/webhook"))
print(webhook.data.url)
```

---

## Error Handling

All HTTP errors are converted into custom exceptions:

| HTTP Code | Exception                          |
| --------- | ---------------------------------- |
| 400       | `BadRequest`                       |
| 401       | `Unauthorized`                     |
| 402       | `PaymentRequired`                  |
| 403       | `Forbidden`                        |
| 404       | `NotFound`                         |
| 422       | `UnprocessableEntity` and subtypes |
| 429       | `TooManyRequests`                  |
| 500       | `InternalServerError`              |

You can catch them individually:

```python
from lalamove.errors import Unauthorized

try:
    sdk.order.get_details("invalid_order_id")
except Unauthorized:
    print("Invalid API credentials.")
```

---

## Enums

### Market

```python
from lalamove.enums import Market

Market.BR  # Brazil
Market.HK  # Hong Kong
# ... others: ID, MY, MX, PH, SG, TW, TH, VN
```

### Language

```python
from lalamove.enums import Language

Language.PT_BR  # Brazilian Portuguese
Language.EN_BR  # English (Brazil)
```

---

## Running in Sandbox

Make sure you are using `sandbox=True` and the corresponding sandbox API key and secret.

---

## Project Structure

```
lalamove/
├── client.py
├── constants.py
├── drivers.py
├── errors.py
├── orders.py
├── quotations.py
├── utils.py
└── webhook.py
```

---

## License

MIT © J. Igor Melo
