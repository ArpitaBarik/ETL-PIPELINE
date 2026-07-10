import polars as pl

# READ ALL TABLES

dim_date = pl.read_parquet(
    "model/dim_date.parquet"
)

dim_geo = pl.read_parquet(
    "model/dim_geo_level.parquet"
)

dim_metro = pl.read_parquet(
    "model/dim_metro_area.parquet"
)

dim_state = pl.read_parquet(
    "model/dim_state.parquet"
)

fact = pl.read_parquet(
    "model/fact_metro.parquet"
)

# NULL VALUE CHECK

print("\nDim Date:")
print(dim_date.null_count())

print("\nDim Geo Level:")
print(dim_geo.null_count())

print("\nDim Metro Area:")
print(dim_metro.null_count())

print("\nDim State:")
print(dim_state.null_count())

print("\nFact Metro:")
print(fact.null_count())

# DUPLICATE ROW CHECK

print(
    "\nDuplicate rows in dim_date:",
    dim_date.is_duplicated().sum()
)

print(
    "Duplicate rows in dim_geo_level:",
    dim_geo.is_duplicated().sum()
)

print(
    "Duplicate rows in dim_metro_area:",
    dim_metro.is_duplicated().sum()
)

print(
    "Duplicate rows in dim_state:",
    dim_state.is_duplicated().sum()
)

print(
    "Duplicate rows in fact_metro:",
    fact.is_duplicated().sum()
)

# PRIMARY KEY UNIQUENESS CHECK

print(
    "\nDuplicate date_id:",
    dim_date["date_id"].is_duplicated().sum()
)

print(
    "Duplicate geo_level_id:",
    dim_geo["geo_level_id"].is_duplicated().sum()
)

print(
    "Duplicate metro_area_id:",
    dim_metro["metro_area_id"].is_duplicated().sum()
)

print(
    "Duplicate state_id:",
    dim_state["state_id"].is_duplicated().sum()
)

print(
    "Duplicate fact_id:",
    fact["fact_id"].is_duplicated().sum()
)

# REFERENTIAL INTEGRITY CHECKS

# date_id validation

missing_dates = fact.join(
    dim_date.select(["date_id"]),
    on="date_id",
    how="anti"
)

print(
    "\nMissing date references:",
    missing_dates.height
)

# metro_area_id validation

missing_metros = fact.join(
    dim_metro.select(["metro_area_id"]),
    on="metro_area_id",
    how="anti"
)

print(
    "Missing metro references:",
    missing_metros.height
)

# geo_level_id validation

missing_geo = fact.join(
    dim_geo.select(["geo_level_id"]),
    on="geo_level_id",
    how="anti"
)

print(
    "Missing geo references:",
    missing_geo.height
)

# ROW COUNT VALIDATION

print("\nDim Date Rows:", dim_date.height)

print(
    "Dim Geo Level Rows:",
    dim_geo.height
)

print(
    "Dim Metro Area Rows:",
    dim_metro.height
)

print(
    "Dim State Rows:",
    dim_state.height
)

print(
    "Fact Metro Rows:",
    fact.height
)

# FINAL VALIDATION RESULT
print("DATA QUALITY VALIDATION COMPLETED SUCCESSFULLY")