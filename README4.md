# US Metro Area ETL Pipeline — End-to-End Project

## Table of Contents
- [Introduction](#introduction)
- [Project Phases](#project-phases)
- [Data Source](#data-source)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Research Phase](#research-phase)
- [ETL Phase](#etl-phase)
- [Data Quality Validation](#data-quality-validation)
- [Analysis Phase](#analysis-phase)
- [Materialized Views](#materialized-views)
- [Data Marts](#data-marts)
- [Reporting Phase](#reporting-phase)
- [License](#license)

---

## Introduction

Welcome to the US Metro Area ETL Pipeline repository. This project is an end-to-end data engineering solution that extracts metropolitan-level socioeconomic data from the **U.S. Census American Community Survey (ACS) API**, transforms and models it into a dimensional star schema, loads it into **PostgreSQL**, validates data quality, and prepares it for analytical reporting.

The three domains analysed across **2019, 2021, and 2022** (Pre-Pandemic → Post-Pandemic) are:

- **Employment** — labor force participation and unemployment rates across metro areas
- **Broadband** — household internet subscription and access types
- **Commute** — transportation modes used by workers

---

## Project Phases

1. **Research** — Identify the correct ACS Census tables and variables for each domain at the metropolitan geography level.
2. **ETL (Extract, Transform, Load)** — Pull raw data from the Census API, clean and type-cast it, build a star schema, and load all dimension and fact tables into PostgreSQL.
3. **Data Quality Validation** — Run null checks, duplicate checks, primary key uniqueness, and referential integrity checks across all tables.
4. **Analysis** — Query the PostgreSQL warehouse using SQL to produce cross-domain insights.
5. **Materialized Views** — Create pre-computed, performance-ready views on top of the star schema.
6. **Data Marts** — Build domain-specific serving tables for business consumption.

---

## Data Source

All data is sourced from the **U.S. Census Bureau — American Community Survey (ACS) 5-Year Estimates**, accessed via the official Census API.

| Domain | ACS Table | Description |
|--------|-----------|-------------|
| Employment | B23025 | Employment Status for Population 16 years and over |
| Broadband | B28002 | Presence and Types of Internet Subscriptions in Household |
| Commute | B08006 | Means of Transportation to Work |

**Years covered:** 2019 · 2021 · 2022

| Year | Period Label |
|------|-------------|
| 2019 | Pre-Pandemic |
| 2021 | Post-Pandemic Year 1 |
| 2022 | Post-Pandemic Year 2 |

**Geography:** Metropolitan Statistical Areas (Metro) and Micropolitan Statistical Areas (Micro) across the United States.

---

## Technologies Used

- **Python** — core pipeline language
- **Polars** — high-performance dataframe processing and transformation
- **US Census API** — data extraction via HTTP requests
- **Apache Parquet** — intermediate columnar storage format
- **PostgreSQL** — relational data warehouse for the final star schema
- **SQLAlchemy** — Python database connector for loading tables into PostgreSQL

---

## Getting Started

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/ArpitaBarik/ETL-PIPELINE.git
   ```

2. Install dependencies:
   ```bash
   pip install polars requests sqlalchemy psycopg2-binary openpyxl
   ```

3. Set your Census API key as an environment variable:
   ```bash
   set CENSUS_API_KEY= "00200b6fdc213ea1ae3272478057c94cb3815637"
   ```

4. Create the target PostgreSQL database:
   ```sql
   CREATE DATABASE metro_pipeline;
   ```

5. Update the database connection string in `src/utils/loading/load_to_postgres.py`:
   ```python
   engine = create_engine(
       "postgresql://postgres:Barik123@localhost:5432/metro_pipeline"
   )
   ```

6. Run the ETL scripts in order:
   ```bash
   python src/utils/modeling/build_dim_date.py
   python src/utils/modeling/build_dim_geo_level.py
   python src/utils/modeling/build_dim_metro_area.py
   python src/utils/modeling/build_dim_state.py
   python src/utils/modeling/build_fact_metro.py
   ```

7. Load all tables into PostgreSQL:
   ```bash
   python src/utils/loading/load_to_postgres.py
   ```

8. Run data quality validation:
   ```bash
   python src/utils/modeling/data_quality_validation.py
   ```

---

## Research Phase

Before writing any code, the correct ACS tables were identified using the official Census API documentation. Tables were selected based on four criteria:

1. Must represent the **entire population** — not a sub-group.
2. Must be **general** — not filtered by race, age, disability, or income.
3. Must contain a **total value** and main breakdown categories.
4. Must be accessible for **metropolitan geography** via the Census API.

### ACS API Call

![API Call](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/01_api_call.png)

### Structured DataFrame Output

![Polars DataFrame](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/02_polars_dataframe.png)

### Selected ACS Variables

**Employment — B23025**

| ACS Variable | Renamed Column |
|---|---|
| B23025_001E | total |
| B23025_002E | in_labor_force |
| B23025_003E | civilian_labor_force |
| B23025_004E | civilian_employed |
| B23025_005E | civilian_unemployed |
| B23025_006E | armed_forces |
| B23025_007E | not_in_labor_force |

**Broadband — B28002**

| ACS Variable | Renamed Column |
|---|---|
| B28002_001E | total_households |
| B28002_002E | with_internet_subscription |
| B28002_004E | broadband_of_any_type |
| B28002_005E | cellular_data_plan |
| B28002_006E | satellite_internet_service |
| B28002_013E | no_internet_access |


**Commute — B08006**

| ACS Variable | Renamed Column |
|---|---|
| B08006_002E | car_truck_or_van |
| B08006_003E | drove_alone |
| B08006_004E | carpooled |
| B08006_005E | public_transportation |
| B08006_006E | bus |
| B08006_007E | subway_or_rail |
| B08006_012E | bicycle |
| B08006_013E | walked |
| B08006_015E | worked_from_home |

Full research documentation: [`ACS_RESEARCH.md`](/ACS_RESEARCH.md)

---

## ETL Phase

Raw Census API data is extracted, cleaned, typed, modeled into a star schema, and loaded into PostgreSQL. Parquet files under `/model` serve as the intermediate warehouse layer.

### DDL — Dimension and Fact Table Schemas

* **dim_date**

![DDL dim_date](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/ddl_dim_date.png)

* **dim_geo_level**

![DDL dim_geo_level](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/ddl_dim_geo_level.png)

* **dim_metro_area**

![DDL dim_metro_area](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/ddl_dim_metro_area.png)

* **dim_state**

![DDL dim_state](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/ddl_dim_state.png)

* **fact_metro**

![DDL fact_metro](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/ddl_fact_metro.png)

---

### ETL Scripts — Dimension Builds

* **dim_date** — `build_dim_date.py`

Covers every calendar day across 2019, 2021, and 2022. Includes `period_label` tagging each year with its pandemic context.

![ETL dim_date](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/etl_dim_date.png)

* **dim_geo_level** — `build_dim_geo_level.py`

Static lookup table distinguishing Metropolitan from Micropolitan Statistical Areas.

![ETL dim_geo_level](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/etl_dim_geo_level.png)

* **dim_metro_area** — `build_dim_metro_area.py`

Extracted from the employment staging file. State code parsed via regex from the metro area name.

![ETL dim_metro_area](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/etl_dim_metro_area.png)

* **dim_state** — `build_dim_state.py`

Derived from the Census state-level population file.

![ETL dim_state](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/etl_dim_state.png)

---

### ETL Script — Fact Table Build

* **fact_metro** — `build_fact_metro.py`

Joins employment, broadband, and commute staging files on `metro_area_id` and `year`. Replaces `year` with `date_id` via a lookup join on `dim_date`. Assigns `geo_level_id` based on whether the metro name contains "Micro Area". Adds surrogate `fact_id` as row index.

![ETL fact_metro](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/etl_fact_metro.png)

---

### Star Schema Diagram

```
                    ┌─────────────┐
                    │  dim_date   │
                    │─────────────│
                    │ date_id (PK)│
                    │ year        │
                    │ quarter     │
                    │ period_label│
                    └──────┬──────┘
                           │
┌──────────────┐    ┌──────┴──────────┐    ┌──────────────────┐
│  dim_state   │    │   fact_metro    │    │  dim_metro_area  │
│──────────────│    │─────────────────│    │──────────────────│
│ state_id (PK)│    │ fact_id (PK)    │    │ metro_area_id(PK)│
│ state_code   │    │ metro_area_id(FK├────│ metro_area_name  │
│ state_name   │    │ geo_level_id(FK)│    │ state_code       │
└──────────────┘    │ date_id (FK)    │    └──────────────────┘
                    │ emp_total       │
                    │ civilian_...    │    ┌──────────────────┐
                    │ broadband_...   │    │  dim_geo_level   │
                    │ commute_...     ├────│──────────────────│
                    └─────────────────┘    │ geo_level_id (PK)│
                                           │ geo_level_name   │
                                           └──────────────────┘
```

---

### Loading into PostgreSQL

After modeling, all Parquet files are pushed to PostgreSQL using SQLAlchemy.

![PostgreSQL Table Load](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/03_postgres_table.png)

---

## Data Quality Validation

`data_quality_validation.py` runs after the full ETL load and checks all five tables across four categories.

### Null Value Check

Verifies no column contains nulls after transformation.

![Null Check](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/dq_null_check.png)

### Duplicate Row Check

Detects any fully duplicated rows across all tables.

![Duplicate Check](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/dq_duplicate_check.png)

### Primary Key Uniqueness Check

Validates that surrogate and natural keys are unique in every table.

![PK Uniqueness Check](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/dq_pk_check.png)

### Referential Integrity Check
 
Confirms every foreign key in `fact_metro` resolves to a valid parent dimension record.

![Referential Integrity Check](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/dq_ref_integrity.png)

### Row Count Summary

![Row Count Summary](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/dq_row_counts.png)

---

## Analysis Phase

The PostgreSQL warehouse is queried using standard SQL against the `metro_pipeline` database.

### Query 1 — Employment recovery by year and pandemic period

```sql
SELECT d.year,
       d.period_label,
       SUM(f.civilian_employed)   AS total_employed,
       SUM(f.civilian_unemployed) AS total_unemployed
FROM fact_metro f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.period_label
ORDER BY d.year;
```

![Employment Recovery Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/analysis_employment_recovery.png)

---

### Query 2 — Broadband access gap: metro vs micro areas

```sql
SELECT g.geo_level_name,
       SUM(f.with_internet_subscription) AS with_internet,
       SUM(f.no_internet_access)         AS no_internet
FROM fact_metro f
JOIN dim_geo_level g ON f.geo_level_id = g.geo_level_id
GROUP BY g.geo_level_name;
```

![Broadband Access Gap Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/analysis_broadband_gap.png)

---

### Query 3 — Work-from-home shift 2019 → 2022 by state

```sql
SELECT s.state_name,
       d.year,
       SUM(f.worked_from_home) AS wfh_workers
FROM fact_metro f
JOIN dim_date       d ON f.date_id       = d.date_id
JOIN dim_metro_area m ON f.metro_area_id = m.metro_area_id
JOIN dim_state      s ON m.state_code    = s.state_code
GROUP BY s.state_name, d.year
ORDER BY s.state_name, d.year;
```

![WFH Shift Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/analysis_wfh_shift.png)

---

### Query 4 — Top 10 metro areas by broadband adoption rate

```sql
SELECT m.metro_area_name,
       ROUND(
           SUM(f.broadband_of_any_type) * 100.0
           / NULLIF(SUM(f.total_households), 0),
       1) AS broadband_pct
FROM fact_metro f
JOIN dim_metro_area m ON f.metro_area_id = m.metro_area_id
GROUP BY m.metro_area_name
ORDER BY broadband_pct DESC
LIMIT 10;
```

![Broadband Adoption Rate Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/analysis_broadband_top10.png)

---

### Query 5 — Commute mode breakdown across all years

```sql
SELECT d.year,
       SUM(f.drove_alone)           AS drove_alone,
       SUM(f.carpooled)             AS carpooled,
       SUM(f.public_transportation) AS public_transit,
       SUM(f.worked_from_home)      AS worked_from_home,
       SUM(f.walked)                AS walked,
       SUM(f.bicycle)               AS bicycle
FROM fact_metro f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;
```

![Commute Mode Breakdown Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/analysis_commute_breakdown.png)

---

### Query Performance — Before and After Indexing

An index is applied on the most frequently joined columns to improve read performance.

```sql
CREATE INDEX idx_fact_date      ON fact_metro (date_id);
CREATE INDEX idx_fact_metro     ON fact_metro (metro_area_id);
CREATE INDEX idx_fact_geo       ON fact_metro (geo_level_id);
```

* Before indexing

![Before Index](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/04_before_index.png)

* After indexing

![After Index](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/05_after_index.png)

* Index creation

![Indexing](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/06_indexing.png)

---

## Materialized Views

Three materialized views are created on top of the star schema in PostgreSQL using `create_materialized_views.sql`. They provide pre-computed, instantly queryable aggregations — making data readily available, consumable, and performance-ready without requiring users to write complex JOINs.

| View | Key Calculated Columns |
|---|---|
| `mv_employment_trend` | `unemployment_rate`, `employment_rate`, `labor_force_participation_rate` |
| `mv_broadband_adoption` | `broadband_adoption_rate`, `no_internet_rate`, `cellular_adoption_rate` |
| `mv_remote_work_pattern` | `wfh_rate`, `drove_alone_rate`, `public_transport_rate`, `carpool_rate` |

### Why Materialized Views

| Property | How Solved |
|---|---|
| Readily Available | Lives in PostgreSQL as a real queryable object |
| Consumable | Pre-joined and pre-aggregated — simple SELECT, no JOIN needed |
| Performance-Ready | Physically stored result — instant reads |

### How to Run

Open `create_materialized_views.sql` in pgAdmin Query Tool and press **F5**.

### Materialized Views Created in pgAdmin

![Materialized Views](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/mv_created.png)

### Refresh When New Data Arrives

```sql
REFRESH MATERIALIZED VIEW mv_employment_trend;
REFRESH MATERIALIZED VIEW mv_broadband_adoption;
REFRESH MATERIALIZED VIEW mv_remote_work_pattern;
```

---

## Data Marts

Three domain-specific data mart tables are built on top of the materialized views using `create_data_mart.sql`. They serve as the final business-ready serving layer before connecting to BI tools like Power BI.

| Table | Source View | Business Question Answered |
|---|---|---|
| `mart_employment` | `mv_employment_trend` | How did employment and unemployment change pre vs post pandemic? |
| `mart_broadband` | `mv_broadband_adoption` | How did broadband access and internet adoption change? |
| `mart_commute` | `mv_remote_work_pattern` | How did commute patterns and work-from-home rates change? |

### How to Run

Open `create_data_mart.sql` in pgAdmin Query Tool and press **F5**.

### Data Mart Tables Created in pgAdmin

![Data Mart Tables](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/data_mart_created.png)

### Sample Query — Work From Home Growth by State

```sql
SELECT state_code,
       MAX(CASE WHEN year = '2019' THEN wfh_rate END) AS wfh_2019,
       MAX(CASE WHEN year = '2022' THEN wfh_rate END) AS wfh_2022,
       ROUND(
           MAX(CASE WHEN year = '2022' THEN wfh_rate END) -
           MAX(CASE WHEN year = '2019' THEN wfh_rate END), 2
       ) AS wfh_growth
FROM mart_commute
GROUP BY state_code
ORDER BY wfh_growth DESC
LIMIT 10;
```

![Data Mart Sample Query](https://github.com/ArpitaBarik/ETL-PIPELINE/blob/dev/screenshots/data_mart_sample_query.png)

---

## Reporting Phase

The reporting layer connects directly to the PostgreSQL metro_pipeline database. All analytical queries from the Analysis Phase serve as the foundation for reporting.

Query results can be exported from pgAdmin using the download button in the Data Output tab as CSV or JSON for use in any reporting tool.

---

## Project File Structure

```
ETL-PIPELINE/
├── src/
│   └── utils/
│       ├── loading/
│       │   └── load_to_postgres.py
│       └── modeling/
│           ├── build_dim_date.py
│           ├── build_dim_geo_level.py
│           ├── build_dim_metro_area.py
│           ├── build_dim_state.py
│           ├── build_fact_metro.py
│           └── data_quality_validation.py
├── output/                          # Staging CSVs from Census API
│   ├── 2019_metro_employment.csv
│   ├── 2021_metro_employment.csv
│   ├── 2022_metro_employment.csv
│   ├── 2019_metro_broadband.csv
│   └── ...
├── model/                           # Intermediate Parquet + CSV files
│   ├── dim_date.parquet / .csv
│   ├── dim_geo_level.parquet / .csv
│   ├── dim_metro_area.parquet / .csv
│   ├── dim_state.parquet / .csv
│   └── fact_metro.parquet / .csv
├── analysis/                        # PostgreSQL query scripts
├── screenshots/                     # All screenshots used in this README
├── create_materialized_views.sql    # Creates 3 materialized views
├── validate_materialized_views.sql  # Validates MV row counts and nulls
├── refresh_materialized_views.sql   # Refreshes MVs when new data arrives
├── create_data_mart.sql             # Creates 3 data mart tables
├── sample_queries.sql               # Ready-to-use business queries
├── ACS_RESEARCH.md
├── pipeline_enhancements.md
└── README.md
```

---

## License

This project is licensed under the MIT License.