import requests
import polars as pl
import os


API_KEY = "00200b6fdc213ea1ae3272478057c94cb3815637"

os.makedirs("output", exist_ok=True)

# MULTIPLE YEARS
YEARS = ["2019", "2021", "2022"]

# METROPOLITAN LEVEL
GEOGRAPHY = "metropolitan statistical area/micropolitan statistical area:*"


def download_table(
    base_url,
    table_name,
    variables,
    output_file,
    column_mapping,
    year
):

    print(f"\nDownloading: {table_name}")
    print(f"Year: {year}")

    params = {
        "get": "NAME," + ",".join(variables),
        "for": GEOGRAPHY,
        "key": API_KEY
    }

    response = requests.get(base_url, params=params)

    response.raise_for_status()

    data = response.json()

    headers = data[0]

    rows = data[1:]

    # Create DataFrame
    df = pl.DataFrame(
        rows,
        schema=headers,
        orient="row"
    )

    # Add year column
    df = df.with_columns(
        pl.lit(year).alias("year")
    )

    # Rename columns
    df = df.rename(column_mapping)

    # Convert numeric columns
    for col in df.columns:

        if col not in ["metro_area", "year", "metro_area_id"]:

            df = df.with_columns(
                pl.col(col).cast(pl.Int64, strict=False)
            )
 
    #null check
    null_counts = df.null_count()
    total_nulls = sum(null_counts.row(0))
    if total_nulls > 0:
        print(f"\nNulls detected after cast in {table_name} ({year}):")
        print(null_counts)
    else:
        print(f"\nNo nulls detected in {table_name} ({year})")

    # Preview
    print("\nPreview:")
    print(df.head())

    # Row count
    print(f"\nTotal Rows: {df.height}")

    # Column count
    print(f"Total Columns: {df.width}")

    # Column names
    print("\nColumns:")
    print(df.columns)

    # Save CSV
    df.write_csv(output_file)

    print(f"\nSaved to {output_file}")


# EMPLOYMENT VARIABLES
employment_vars = [
    "B23025_001E",
    "B23025_002E",
    "B23025_003E",
    "B23025_004E",
    "B23025_005E",
    "B23025_006E",
    "B23025_007E"
]

employment_column_mapping = {

    "NAME": "metro_area",

    "B23025_001E": "total",

    "B23025_002E": "in_labor_force",

    "B23025_003E": "civilian_labor_force",

    "B23025_004E": "civilian_employed",

    "B23025_005E": "civilian_unemployed",

    "B23025_006E": "armed_forces",

    "B23025_007E": "not_in_labor_force",

    "metropolitan statistical area/micropolitan statistical area":
        "metro_area_id"
}



# BROADBAND VARIABLES
broadband_vars = [
    "B28002_001E",
    "B28002_002E",
    "B28002_003E",
    "B28002_004E",
    "B28002_005E",
    "B28002_006E",
    "B28002_007E",
    "B28002_008E",
    "B28002_009E",
    "B28002_010E",
    "B28002_011E",
    "B28002_012E",
    "B28002_013E"
]

broadband_column_mapping = {

    "NAME": "metro_area",

    "B28002_001E": "total",

    "B28002_002E": "with_internet_subscription",

    "B28002_003E":
        "dial_up_with_no_other_internet_subscription",

    "B28002_004E":
        "broadband_of_any_type",

    "B28002_005E":
        "cellular_data_plan",

    "B28002_006E":
        "cellular_data_plan_only",

    "B28002_007E":
        "broadband_cable_fiber_or_dsl",

    "B28002_008E":
        "broadband_cable_fiber_or_dsl_only",

    "B28002_009E":
        "satellite_internet_service",

    "B28002_010E":
        "satellite_internet_service_only",

    "B28002_011E":
        "other_service_only",

    "B28002_012E":
        "internet_access_without_subscription",

    "B28002_013E":
        "no_internet_access",

    "metropolitan statistical area/micropolitan statistical area":
        "metro_area_id"
}



commute_vars = [
    "B08006_001E",   
    "B08006_002E",   
    "B08006_003E",   
    "B08006_004E",  
    "B08006_005E",  
    "B08006_006E",   
    "B08006_007E",   
    "B08006_008E",   
    "B08006_009E",   
    "B08006_010E",   
    "B08006_011E",   
    "B08006_012E",   
    "B08006_013E",   
    "B08006_014E",   
    "B08006_015E",   
    "B08006_016E",   
    "B08006_017E"    
]
commute_column_mapping = {

    "NAME": "metro_area",
    "B08006_001E": "total_workers",
    "B08006_002E": "car_truck_or_van",
    "B08006_003E": "drove_alone",
    "B08006_004E": "carpooled",
    "B08006_005E": "public_transportation",
    "B08006_006E": "bus",
    "B08006_007E": "long_distance_train_or_commuter_rail",
    "B08006_008E": "light_rail_streetcar_or_trolley",
    "B08006_009E": "ferryboat",
    "B08006_010E": "taxicab",
    "B08006_011E": "motorcycle",
    "B08006_012E": "bicycle",
    "B08006_013E": "walked",
    "B08006_014E": "other_means",
    "B08006_015E": "worked_from_home",
    "B08006_016E": "other_aggregate",
    "B08006_017E": "worked_from_home_extended",
    "metropolitan statistical area/micropolitan statistical area": "metro_area_id"
}



#LOOP
for year in YEARS:

    BASE_URL = f"https://api.census.gov/data/{year}/acs/acs5"

    print(f"\nProcessing Year: {year}")

    #Employment table 
    try:
        download_table(
            BASE_URL,
            "Employment (B23025)",
            employment_vars,
            f"output/{year}_metro_employment.csv",
            employment_column_mapping,
            year
        )
    except Exception as e:
        print(f"Failed: Employment (B23025) for {year}: {e}")

    #Broadband table
    try:
        download_table(
            BASE_URL,
            "Broadband (B28002)",
            broadband_vars,
            f"output/{year}_metro_broadband.csv",
            broadband_column_mapping,
            year
        )
    except Exception as e:
        print(f"Failed: Broadband (B28002) for {year}: {e}")
 
    # Commute table
    try:
        download_table(
            BASE_URL,
            "Commute (B08006)",
            commute_vars,
            f"output/{year}_metro_commute.csv",
            commute_column_mapping,
            year
        )
    except Exception as e:
        print(f"Failed: Commute (B08006) for {year}: {e}")

print("\nALL TABLES DOWNLOADED SUCCESSFULLY")