import polars as pl
import os


def build_dim_metro_area():

    # Read employment file
    employment = pl.read_csv(
        "output/metro_employment.csv"
    )

    # Select required columns
    dim_metro_area = (
        employment
        .select([
            "metro_area_id",
            "metro_area"
        ])

        # Remove duplicate metro areas
        .unique(
            subset=["metro_area_id"]
        )

        # Extract state code
        .with_columns(

            pl.col("metro_area")

            .str.extract(
                r",\s([A-Z]{2})",
                group_index=1
            )

            .alias("state_code")
        )

        # Rename column
        .rename({
            "metro_area":
                "metro_area_name"
        })

        # Sort by metro_area_id
        .sort("metro_area_id")
    )

    return dim_metro_area



dim_metro_area = build_dim_metro_area()

print(dim_metro_area.head())

print(f"\nRows: {dim_metro_area.height}")

print(f"Columns: {dim_metro_area.width}")



os.makedirs("model",exist_ok=True)

# Save files
dim_metro_area.write_parquet(
    "model/dim_metro_area.parquet"
)

dim_metro_area.write_csv(
    "model/dim_metro_area.csv"
)

print("\nDimension saved successfully!")