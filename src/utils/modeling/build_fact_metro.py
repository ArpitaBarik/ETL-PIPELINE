import polars as pl
import os


def build_fact_metro():

    # READ SOURCE FILES (ALL YEARS)
   
    employment = pl.concat([

        pl.read_csv("output/2019_metro_employment.csv"),

        pl.read_csv("output/2021_metro_employment.csv"),

        pl.read_csv("output/2022_metro_employment.csv")

    ])

    broadband = pl.concat([

        pl.read_csv("output/2019_metro_broadband.csv"),

        pl.read_csv("output/2021_metro_broadband.csv"),

        pl.read_csv("output/2022_metro_broadband.csv")

    ])

    commute = pl.concat([

        pl.read_csv("output/2019_metro_commute.csv"),

        pl.read_csv("output/2021_metro_commute.csv"),

        pl.read_csv("output/2022_metro_commute.csv")

    ])

    dim_date = pl.read_parquet(
        "model/dim_date.parquet"
    )

    # PREPARE EMPLOYMENT TABLE
    
    employment = (

        employment

        .with_columns(

            pl.when(
                pl.col("metro_area")
                .str.contains("Micro Area")
            )

            .then(pl.lit(2))

            .otherwise(pl.lit(1))

            .alias("geo_level_id")
        )

        .rename({
            "total": "emp_total"
        })

        .drop("metro_area")
    )

    # PREPARE BROADBAND TABLE
    
    broadband = (

        broadband

        .rename({
            "total": "brd_total"
        })

        .drop("metro_area")
    )

    # PREPARE COMMUTE TABLE
  
    commute = commute.drop("metro_area")

    # JOIN ALL FACT SOURCES
  
    fact = (

        employment

        .join(
            broadband,
            on=["metro_area_id", "year"],
            how="inner"
        )

        .join(
            commute,
            on=["metro_area_id", "year"],
            how="inner"
        )
    )

    # CREATE YEAR LOOKUP FROM DIM_DATE
   
    year_lookup = (

        dim_date

        .filter(
            pl.col("is_year_start") == True
        )

        .select([
            pl.col("year").cast(pl.Int64),
            "date_id"
        ])
    )

    # ADD DATE_ID TO FACT TABLE

    fact = (

        fact

        .with_columns(
            pl.col("year").cast(pl.Int64)
        )

        .join(
            year_lookup,
            on="year",
            how="left"
        )

        .drop("year")
    )

    
    # ADD FACT SURROGATE KEY
    

    fact = fact.with_row_index(
        name="fact_id",
        offset=1
    )

    return fact

# EXECUTE

fact_metro = build_fact_metro()

print("\nFACT TABLE PREVIEW:")
print(fact_metro.head())

print(f"\nRows: {fact_metro.height}")
print(f"Columns: {fact_metro.width}")

# SAVE OUTPUT

os.makedirs(
    "model",
    exist_ok=True
)

fact_metro.write_parquet(
    "model/fact_metro.parquet"
)

fact_metro.write_csv(
    "model/fact_metro.csv"
)

print("\nFact table saved successfully!")