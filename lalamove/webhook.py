from lalamove.client import APIClient
from pydantic import BaseModel


class WebhookData(BaseModel):
    url: str


class WebhookBody(BaseModel):
    data: WebhookData


class WebhookResponseData(BaseModel):
    url: str


class WebhookResponse(BaseModel):
    data: WebhookResponseData


class Webhook:
    def __init__(self, client: APIClient):
        self.client = client

    def set_webhook(self, url: str):
        data = WebhookBody(data=WebhookData(url=url))
        response = self.client.make_request("PATCH", "webhook", data.model_dump())
        return WebhookResponse.model_validate({"data": response})
