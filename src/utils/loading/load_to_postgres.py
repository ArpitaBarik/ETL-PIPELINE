from sqlalchemy import create_engine
import polars as pl

# CREATE POSTGRES CONNECTION

engine = create_engine(
    "postgresql://postgres:Arpita123@localhost:5432/census_dw"
)

# READ STAR SCHEMA TABLES

dim_date = pl.read_parquet(
    "model/dim_date.parquet"
)

dim_geo_level = pl.read_parquet(
    "model/dim_geo_level.parquet"
)

dim_metro_area = pl.read_parquet(
    "model/dim_metro_area.parquet"
)

dim_state = pl.read_parquet(
    "model/dim_state.parquet"
)

fact_metro = pl.read_parquet(
    "model/fact_metro.parquet"
)

# LOAD TABLES TO POSTGRES

print("Loading dim_date...")

dim_date.to_pandas().to_sql(
    "dim_date",
    engine,
    if_exists="replace",
    index=False
)

print("Loading dim_geo_level...")

dim_geo_level.to_pandas().to_sql(
    "dim_geo_level",
    engine,
    if_exists="replace",
    index=False
)

print("Loading dim_metro_area...")

dim_metro_area.to_pandas().to_sql(
    "dim_metro_area",
    engine,
    if_exists="replace",
    index=False
)

print("Loading dim_state...")

dim_state.to_pandas().to_sql(
    "dim_state",
    engine,
    if_exists="replace",
    index=False
)

print("Loading fact_metro...")

fact_metro.to_pandas().to_sql(
    "fact_metro",
    engine,
    if_exists="replace",
    index=False
)

print("\nAll tables loaded successfully into PostgreSQL!")