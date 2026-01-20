"""
Validate HTTP contracts against a running local server.
Requires ORIGIN_VERIFY_SECRET in env.
"""

import json
import os
import sys
from urllib import request
from urllib.error import HTTPError, URLError


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
ORIGIN = "http://localhost:5173"
DEFAULT_ENV_PATH = os.getenv("ENV_PATH", ".env")


def load_env_file(path):
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def make_request(method, path, headers=None, body=None):
    url = f"{BASE_URL}{path}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req_headers = {"Origin": ORIGIN}
    if headers:
        req_headers.update(headers)
    req = request.Request(url, data=data, method=method, headers=req_headers)
    try:
        with request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read()
    except HTTPError as exc:
        return exc.code, exc.read()
    except URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def assert_key(payload, key):
    if key not in payload:
        raise AssertionError(f"Missing key '{key}' in payload: {payload}")


def validate_post_contact(secret):
    headers = {
        "Content-Type": "application/json",
        "X-Origin-Verify": secret,
    }
    body = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "company": "Analytical Engines",
        "message": "Hello",
        "page_location": "/",
        "traffic_source": "direct",
    }
    status, raw = make_request("POST", "/v1/contact/email", headers=headers, body=body)
    if status != 201:
        raise AssertionError(f"POST /v1/contact/email expected 201, got {status}: {raw}")
    payload = json.loads(raw.decode("utf-8"))
    assert_key(payload, "ticket_id")


def validate_post_contact_invalid(secret):
    headers = {
        "Content-Type": "application/json",
        "X-Origin-Verify": secret,
    }
    body = {
        "name": "",
        "email": "ada@example.com",
        "company": "",
        "message": "",
        "page_location": "",
        "traffic_source": "",
    }
    status, raw = make_request("POST", "/v1/contact/email", headers=headers, body=body)
    if status != 400:
        raise AssertionError(f"POST invalid expected 400, got {status}: {raw}")
    payload = json.loads(raw.decode("utf-8"))
    assert_key(payload, "error_code")
    if payload["error_code"] != "MISSING_FIELDS":
        raise AssertionError(f"Expected error_code MISSING_FIELDS, got {payload['error_code']}")


def validate_get_list(secret):
    headers = {"X-Origin-Verify": secret}
    status, raw = make_request("GET", "/v1/contact/list", headers=headers)
    if status != 200:
        raise AssertionError(f"GET /v1/contact/list expected 200, got {status}: {raw}")
    payload = json.loads(raw.decode("utf-8"))
    assert_key(payload, "success")
    assert_key(payload, "contactos")
    if not isinstance(payload["contactos"], list):
        raise AssertionError("contactos is not a list")


def main():
    load_env_file(DEFAULT_ENV_PATH)
    secret = os.getenv("ORIGIN_VERIFY_SECRET")
    if not secret:
        print("Missing ORIGIN_VERIFY_SECRET in environment or .env.")
        return 1

    validate_post_contact(secret)
    validate_post_contact_invalid(secret)
    validate_get_list(secret)
    print("Endpoint validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
