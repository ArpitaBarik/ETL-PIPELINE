import os
import pandas as pd
from urllib.parse import urlencode

from src.utils.helpers.api_download_helpers import request_api, APIRequestError


# -----------------------------------
# CONFIGURATION
# -----------------------------------
CENSUS_API_URL = "https://api.census.gov/data/2022/acs/acs5"
CENSUS_API_KEY = os.getenv(
    "CENSUS_API_KEY",
    "00200b6fdc213ea1ae3272478057c94cb3815637"
)

VARIABLE_LABELS = {
    "NAME": "State Name",
    "B01003_001E": "Total Population",
    "state": "State Code"
}

PARAMS = {
    "get": "NAME,B01003_001E",
    "for": "state:*",
    "key": CENSUS_API_KEY
}


# -----------------------------------
# MAIN LOGIC
# -----------------------------------
def main():
    
    full_url = CENSUS_API_URL + "?" + urlencode(PARAMS)
    print("\nAPI URL:")
    print(full_url)
    print("-" * 80)

    try:
        
        status, payload = request_api(
            method="GET",
            url=CENSUS_API_URL,
            params=PARAMS,
            headers={"Accept": "application/json"},
            timeout=8,
            retries=3
        )

        print(f"Status Code: {status}")

       
        if not payload or len(payload) < 2:
            raise ValueError("Empty or invalid API response")

       
        headers = payload[0]
        rows = payload[1:]

        df = pd.DataFrame(rows, columns=headers)
        df.rename(columns=VARIABLE_LABELS, inplace=True)

        df["Total Population"] = pd.to_numeric(
            df["Total Population"], errors="coerce"
        )

        print("\nStructured DataFrame (first 5 rows):")
        print(df.head())

        
        print("\nPopulation Statistics:")
        print(f"Total US Population: {df['Total Population'].sum():,}")
        print(f"Average State Population: {df['Total Population'].mean():,.0f}")

      
        os.makedirs("output", exist_ok=True)
        output_file = "output/census_population_by_state.csv"
        df.to_csv(output_file, index=False)

        print(f"\nData saved to: {output_file}")

    except APIRequestError as err:
        print("API request failed:", err)
    except Exception as exc:
        print("Unexpected error:", exc)


# -----------------------------------
# ENTRY POINT
# -----------------------------------
if __name__ == "__main__":
    main()
