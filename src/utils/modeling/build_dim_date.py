import polars as pl
import datetime
import os


YEARS = ["2019", "2021", "2022"]

PERIOD_LABELS = {
    "2019": "Pre-Pandemic",
    "2021": "Post-Pandemic Year 1",
    "2022": "Post-Pandemic Year 2"
}


def build_dim_date():

    rows = []
    date_id = 1

    for year_str in YEARS:

        year = int(year_str)

        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        current = start_date

        while current <= end_date:

            rows.append({

                "date_id": date_id,

                "full_date": current.isoformat(),

                "day": current.day,

                "day_name": current.strftime("%A"),

                "day_of_week": current.isoweekday(),

                "week_of_year": current.isocalendar()[1],

                "month": current.month,

                "month_name": current.strftime("%B"),

                "quarter": f"Q{((current.month - 1)//3)+1}",

                "year": year,

                "decade": f"{(year//10)*10}s",

                "is_weekend":
                    current.isoweekday() in [6, 7],

                "is_leap_year":
                    year % 4 == 0 and
                    (year % 100 != 0 or year % 400 == 0),

                "is_year_start":
                    current.month == 1 and current.day == 1,

                "period_label":
                    PERIOD_LABELS[year_str]
            })

            date_id += 1

            current += datetime.timedelta(days=1)

    dim_date = pl.DataFrame(rows)

    return dim_date

dim_date = build_dim_date()

print(dim_date.head())

print(f"\nRows: {dim_date.height}")

os.makedirs("model", exist_ok=True)

dim_date.write_parquet(
    "model/dim_date.parquet"
)

dim_date.write_csv(
    "model/dim_date.csv"
)
print("\nDimension saved successfully!")