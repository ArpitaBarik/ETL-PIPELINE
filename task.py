from src.utils.helpers.api_download_helpers import request_api, APIRequestError

CENSUS_API_URL = "https://api.census.gov/data/2022/acs/acs5"
CENSUS_API_KEY = "00200b6fdc213ea1ae3272478057c94cb3815637"

try:
    status, data = request_api(
        method="GET",
        url=CENSUS_API_URL,
        params={
            "get": "NAME,B01003_001E",
            "for": "state:*",
            "key": CENSUS_API_KEY
        },
        headers={
            "Accept": "application/json"
        },
        timeout=8,
        retries=3
    )

    print("Status:", status)
    print("Data:")
    for row in data[:5]:
        print(row)



except APIRequestError as error:
    print("API request failed:", error)
