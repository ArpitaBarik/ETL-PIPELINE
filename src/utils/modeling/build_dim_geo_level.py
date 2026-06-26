import polars as pl
import os


def build_dim_geo_level():

    dim_geo_level = pl.DataFrame({

        "geo_level_id": [1, 2],

        "geo_level_name": [
            "Metropolitan Statistical Area",
            "Micropolitan Statistical Area"
        ]
    })

    return dim_geo_level


dim_geo_level = build_dim_geo_level()

print(dim_geo_level)

print(f"\nRows: {dim_geo_level.height}")



os.makedirs("model", exist_ok=True)


dim_geo_level.write_parquet(
    "model/dim_geo_level.parquet"
)

dim_geo_level.write_csv(
    "model/dim_geo_level.csv"
)

print("\nDimension saved successfully!")