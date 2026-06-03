import os
from src.utils.helpers.api_download_helpers import request_api, APIRequestError
from urllib.parse import urlencode

# Census API details
CENSUS_API_URL = "https://api.census.gov/data/2022/acs/acs5"
# Better: Load from environment variable (falls back to hardcoded for development)
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "00200b6fdc213ea1ae3272478057c94cb3815637")

# API parameters
params = {
    "get": "NAME,B01003_001E",
    "for": "state:*",
    "key": CENSUS_API_KEY
}

# Print the full URL for debugging
full_url = CENSUS_API_URL + "?" + urlencode(params)
print("API URL:")
print(full_url)
print("-" * 50)

try:
    # Make the API request
    status, payload = request_api(
        method="GET",
        url=CENSUS_API_URL,
        params=params,
        headers={
            "Accept": "application/json"
        },
        timeout=8,
        retries=4
    )
    
    # Check status code
    if status != 200:
        print(f"Warning: Received status code {status}")
    
    # Validate response
    if not payload or len(payload) < 2:
        print("Warning: Empty or invalid response")
    else:
        print("Status Code:", status)
        print(f"Found {len(payload) - 1} states")  # -1 for header row
        print("\nSample Census Data:")
        for row in payload[:5]:
            print(row)
            
except APIRequestError as err:
    print("Request failed:", err)
except Exception as e:
    print(f"Unexpected error: {e}")
