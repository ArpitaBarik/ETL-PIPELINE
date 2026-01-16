# Census Population Data Project

A Python project that fetches US Census population data via API, processes it using Polars, and exports the results to CSV.

## Project Overview

This project demonstrates working with REST APIs, handling JSON responses, data transformation, and basic statistical analysis using real-world Census Bureau data.

## What Has Been Done So Far

### 1. API Integration
- Created helper function to fetch data from US Census API
- Implemented API call with proper parameters (state name, population variable, geographic level)
- Added API key authentication

### 2. Data Processing
- Parsed JSON response from the API
- Converted raw JSON into structured Polars DataFrame
- Renamed census variable codes to readable column names:
  1.NAME → State Name
  2.B01003_001E → Total Population
  3.state → State Code

### 3. Data Analysis
- Converted population data to integer type for calculations
- Calculated total US population (sum of all states)
- Calculated average population per state

### 4. Data Export
- Created output directory structure
- Saved processed data as CSV file for future use

## Technologies Used

1.Python 
2.Requests - for API calls
3.Polars - for data processing
4.US Census API - data source

## Key Features

- Reusable API helper functions
- Clean the data and transform
- Statistical calculations
- CSV export functionality

## Current Output


- Full API URL with encoded parameters
- HTTP status code
- Preview of structured DataFrame (first 5 rows)
- Total US population
- Average state population
- Confirmation of CSV file creation

