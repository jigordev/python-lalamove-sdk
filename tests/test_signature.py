from lalamove.auth import get_auth_token
from unittest.mock import patch
import hmac
import hashlib


@patch("lalamove.auth.time")
def test_get_auth_token(mock_time):
    mock_time.time.return_value = 1735689600.0

    method = "GET"
    path = "quotations"
    body = ""
    api_key = "api_key"
    api_secret = "api_secret"
    timestamp = "1735689600000"

    raw = f"{timestamp}\r\n{method}\r\n/{path}\r\n\r\n{body}"
    signature = hmac.new(api_secret.encode(), raw.encode(), hashlib.sha256).hexdigest()
    expected_token = f"{api_key}:{timestamp}:{signature}"

    generated_token = get_auth_token(api_key, api_secret, method, f"/{path}", body)
    assert expected_token == generated_token
