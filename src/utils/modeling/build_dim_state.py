import polars as pl
import os


def build_dim_state():

    # Read state population file
    state_raw = pl.read_csv(
        "output/census_population_by_state.csv"
    )

    dim_state = (

        state_raw
        .select([
            "State Code",
            "State Name"
            ])
        .unique()
        
        .rename({
            "State Code": "state_code",
            "State Name": "state_name"
            })

        .sort("state_code")

        .with_row_index(
            name="state_id",
            offset=1
        )
    )

    return dim_state


dim_state = build_dim_state()

print(dim_state.head())

print(f"\nRows: {dim_state.height}")

print(f"Columns: {dim_state.width}")


os.makedirs("model",exist_ok=True)


dim_state.write_parquet(
    "model/dim_state.parquet"
)

dim_state.write_csv(
    "model/dim_state.csv"
)

print("\nDimension saved successfully!")