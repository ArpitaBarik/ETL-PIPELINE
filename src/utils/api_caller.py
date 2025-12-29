from src.utils.helpers.api_download_helpers import request_api, APIRequestError

try:
    status, payload = request_api(
        method="GET",
        url="https://api.example.com/data",
        params={"page": 1},
        headers={"Accept": "application/json"},
        timeout=8,
        retries=4,
    )
    print(status, payload)
except APIRequestError as err:
    print("Request failed:", err)