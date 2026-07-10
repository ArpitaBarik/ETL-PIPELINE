import os
from urllib.parse import urlencode

import polars as pl

from src.utils.helpers.api_download_helpers import request_api, APIRequestError


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

        df = pl.DataFrame(
            rows,
            schema=headers,
            orient="row"   
        )

        df = df.rename(VARIABLE_LABELS)

        df = df.with_columns(
            pl.col("Total Population").cast(pl.Int64, strict=False)
        )

        print("\nStructured DataFrame (first 5 rows):")
        print(df.head())

        total_population = df.select(
            pl.col("Total Population").sum()
        ).item()

        avg_population = df.select(
            pl.col("Total Population").mean()
        ).item()

        print("\nPopulation Statistics:")
        print(f"Total US Population: {total_population:,}")
        print(f"Average State Population: {avg_population:,.0f}")

        os.makedirs("output", exist_ok=True)
        df.write_csv("output/census_population_by_state.csv")

        print("\nData saved to: output/census_population_by_state.csv")

    except APIRequestError as err:
        print("API request failed:", err)

    except Exception as exc:
        print("Unexpected error:", exc)


if __name__ == "__main__":
    main()
