import requests
import polars as pl


# CONFIG

API_KEY = "00200b6fdc213ea1ae3272478057c94cb3815637"
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"

# METROPOLITAN LEVEL
GEOGRAPHY = "metropolitan statistical area/micropolitan statistical area:*"


# COMMON FUNCTION

def download_table(table_name, variables, output_file):

    
    print(f"Downloading: {table_name}")

    params = {
        "get": "NAME," + ",".join(variables),
        "for": GEOGRAPHY,
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    headers = data[0]
    rows = data[1:]

    df = pl.DataFrame(rows, schema=headers, orient="row")

    # Convert numeric columns
    for col in df.columns:
        if col != "NAME":
            df = df.with_columns(pl.col(col).cast(pl.Int64, strict=False))

    print("\nPreview:")
    print(df.head())

    print(f"\nTotal metro rows: {df.height}")

    df.write_csv(output_file)

    print(f"\nSaved to {output_file}")



# EMPLOYMENT (B23025)

employment_vars = [
    "B23025_001E","B23025_002E","B23025_003E",
    "B23025_004E","B23025_005E","B23025_006E","B23025_007E"
]

download_table(
    "Employment (B23025)",
    employment_vars,
    "output/metro_employment.csv"
)



# BROADBAND (B28002)

broadband_vars = [
    "B28002_001E","B28002_002E","B28002_003E","B28002_004E",
    "B28002_005E","B28002_006E","B28002_007E","B28002_008E",
    "B28002_009E","B28002_010E","B28002_011E","B28002_012E",
    "B28002_013E"
]

download_table(
    "Broadband (B28002)",
    broadband_vars,
    "output/metro_broadband.csv"
)



# B08006 FULL RANGE

commute_vars = [
    "B08006_001E","B08006_002E","B08006_003E","B08006_004E",
    "B08006_005E","B08006_006E","B08006_007E","B08006_008E",
    "B08006_009E","B08006_010E","B08006_011E","B08006_012E",
    "B08006_013E","B08006_014E","B08006_015E"
]

download_table(
    "Commute (B08006)",
    commute_vars,
    "output/metro_commute.csv"
)



print("ALL TABLES DOWNLOADED SUCCESSFULLY")
