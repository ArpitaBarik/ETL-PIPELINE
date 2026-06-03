import requests
import polars as pl


API_KEY = "00200b6fdc213ea1ae3272478057c94cb3815637"

# MULTIPLE YEARS
YEARS = ["2020", "2021", "2022"]

# METROPOLITAN LEVEL
GEOGRAPHY = "metropolitan statistical area/micropolitan statistical area:*"


def download_table(
    base_url,
    table_name,
    variables,
    csv_file,
    parquet_file,
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

        if col not in ["metro_area", "year"]:

            df = df.with_columns(
                pl.col(col).cast(pl.Int64, strict=False)
            )

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
    df.write_csv(csv_file)

     # Save Parquet
    df.write_parquet(parquet_file)

    print(f"\nSaved to {csv_file}")

    print(f"Parquet Saved: {parquet_file}")


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



# COMMUTE VARIABLES
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
    "B08006_015E"
]

commute_column_mapping = {

    "NAME": "metro_area",

    "B08006_001E": "total_workers",

    "B08006_002E": "car_truck_or_van",

    "B08006_003E": "drove_alone",

    "B08006_004E": "carpooled",

    "B08006_005E": "public_transportation",

    "B08006_006E": "bus",

    "B08006_007E": "subway_or_rail",

    "B08006_008E": "taxi",

    "B08006_009E": "motorcycle",

    "B08006_010E": "bicycle",

    "B08006_011E": "walked",

    "B08006_012E": "other_means",

    "B08006_013E": "worked_from_home",

    "B08006_014E": "other",

    "B08006_015E": "worked_from_home_extended",

    "metropolitan statistical area/micropolitan statistical area":
        "metro_area_id"
}

# DATATYPE DOCUMENTATION

datatype_mapping = {

    # COMMON COLUMNS
    "metro_area": "String",

    "metro_area_id": "String/Int64",

    "year": "Int64",

    # EMPLOYMENT TABLE
    "total": "Int64",

    "in_labor_force": "Int64",

    "civilian_labor_force": "Int64",

    "civilian_employed": "Int64",

    "civilian_unemployed": "Int64",

    "armed_forces": "Int64",

    "not_in_labor_force": "Int64",

    # BROADBAND TABLE
    "with_internet_subscription": "Int64",

    "dial_up_with_no_other_internet_subscription": "Int64",

    "broadband_of_any_type": "Int64",

    "cellular_data_plan": "Int64",

    "cellular_data_plan_only": "Int64",

    "broadband_cable_fiber_or_dsl": "Int64",

    "broadband_cable_fiber_or_dsl_only": "Int64",

    "satellite_internet_service": "Int64",

    "satellite_internet_service_only": "Int64",

    "other_service_only": "Int64",

    "internet_access_without_subscription": "Int64",

    "no_internet_access": "Int64",

    # COMMUTE TABLE
    "total_workers": "Int64",

    "car_truck_or_van": "Int64",

    "drove_alone": "Int64",

    "carpooled": "Int64",

    "public_transportation": "Int64",

    "bus": "Int64",

    "subway_or_rail": "Int64",

    "taxi": "Int64",

    "motorcycle": "Int64",

    "bicycle": "Int64",

    "walked": "Int64",

    "other_means": "Int64",

    "worked_from_home": "Int64",

    "other": "Int64",

    "worked_from_home_extended": "Int64"
}

datatype_df = pl.DataFrame({

    "column_name": list(datatype_mapping.keys()),

    "datatype": list(datatype_mapping.values())
})

print("\nDatatype Documentation:")

print(datatype_df)


#LOOP
for year in YEARS:

    BASE_URL = f"https://api.census.gov/data/{year}/acs/acs5"

    print(f"\nProcessing Year: {year}")

    #Employment table 
    download_table(
        BASE_URL,
        "Employment (B23025)",
        employment_vars,
        f"output/{year}_metro_employment.csv",
        f"output/{year}_metro_employment.parquet",
        employment_column_mapping,
        year
    )
    #Broadband table
    download_table(
        BASE_URL,
        "Broadband (B28002)",
        broadband_vars,
        f"output/{year}_metro_broadband.csv",
        f"output/{year}_metro_broadband.parquet",
        broadband_column_mapping,
        year
    )

    #commute table
    download_table(
        BASE_URL,
        "Commute (B08006)",
        commute_vars,
        f"output/{year}_metro_commute.csv",
        f"output/{year}_metro_commute.parquet",
        commute_column_mapping,
        year
    )


print("\nALL TABLES DOWNLOADED SUCCESSFULLY")