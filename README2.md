# Census API Data Processing and Performance Optimization

This project shows a simple end-to-end data workflow using a public API, data processing with Polars, and basic database performance optimization using PostgreSQL.


## Project Objective

The objective of this project is to:

- Fetch data from an external API
- Clean and structure the data using Polars
- Load the cleaned data into PostgreSQL
- Apply indexing to improve read performance
- Compare query performance before and after indexing

All steps are implemented and demonstrated inside a Jupyter Notebook.


## Step-by-Step Workflow

### 1. API Data Extraction

State-level population data is fetched from the US Census API.
The API response is received in JSON format.

[API Call](screenshots/01_api_call.png)


### 2. Data Cleaning and Transformation (Polars)

The raw JSON data is converted into a structured Polars DataFrame.
Column names are renamed to meaningful names and population values are converted to numeric types.

[Polars DataFrame](screenshots/02_polars_dataframe.png)


### 3. Load Data into PostgreSQL

The cleaned data is loaded into a PostgreSQL table named `census_population`.
The data load is verified using SQL queries.

[PostgreSQL Table](screenshots/03_postgres_table.png)


### 4. Query Performance Before Indexing

A SELECT query is executed to filter states with a population greater than 10 million.
The query execution time is measured before any index is applied.

[Before Index](screenshots/04_before_index.png)


### 5. Index Creation and Query Performance After Indexing

An index is created on the `total_population` column.
The same query is executed again and the execution time is measured.
[Indexing](screenshots/06_indexing.png)
[After Index](screenshots/05_after_index.png)


## Performance Comparison Summary

The number of rows returned remains the same.
The difference in execution time is small after indexing because the dataset is small.


## Technologies Used

- Python
- Jupyter Notebook
- Polars
- PostgreSQL
- SQLAlchemy
- US Census API

## Conclusion

This project demonstrates how indexing affects database read performance.
Although the dataset is small, the workflow correctly shows how indexing improves query execution and how such optimizations become more important as data size grows.
