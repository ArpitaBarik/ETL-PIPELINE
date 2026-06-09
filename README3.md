# Census ACS Metro Data Pipeline

## Overview

This project extracts metropolitan-level data from the U.S. Census American Community Survey(ACS) . The data is collected for three domains:

* Employment
* Broadband 
* commute

The extracted data is cleaned, converted into appropriate datatypes, and stored as staging datasets for further analysis and data modeling.

---
# Data Source

Official ACS API Documentation:

* Employment (B23025):
  https://api.census.gov/data/2022/acs/acs5/groups/B23025.html

* Broadband (B28002):
  https://api.census.gov/data/2022/acs/acs5/groups/B28002.html

* Commute (B08006):
  https://api.census.gov/data/2022/acs/acs5/groups/B08006.html

---

# Datatype Justification

1. metro_area

Source Column: NAME

Datatype: String

Justification: The NAME field contains the descriptive name of the metropolitan or micropolitan area (e.g. "Abilene, TX Metro Area"). Since this field stores textual information rather than numeric values, the String datatype is used.
---

2. metro_area_id

Source Column: metropolitan statistical area/micropolitan statistical area

Datatype: Int64

Justification: This column contains the unique Census geographic identifier assigned to each metropolitan or micropolitan area. Since the values are numeric identifiers, Int64 is the appropriate datatype.

3. Employment Variables (B23025)

Examples:

total
in_labor_force
civilian_labor_force
civilian_employed
civilian_unemployed
armed_forces
not_in_labor_force

Datatype: Int64

Justification: According to the ACS B23025 documentation, these fields represent population counts. Population counts are whole numbers and do not contain decimal values. Therefore, Int64 is used to accurately store large numeric values and support future calculations, and analytical operations.

4. Broadband Variables (B28002)

Examples:

with_internet_subscription
broadband_of_any_type
cellular_data_plan
satellite_internet_service
no_internet_access

Datatype:Int64

Justification: The ACS B28002 table represents counts of households categorized by internet subscription type. Since these fields store household counts rather than percentages or text values, Int64 is used to preserve numerical accuracy and enable statistical analysis.

5. Commute Variables (B08006)

Examples:

drove_alone
carpooled
public_transportation
bus
subway_or_rail
bicycle
walked
worked_from_home

Datatype: Int64

Justification: The ACS B08006 table contains counts of workers grouped by transportation method. These values are discrete numeric counts and are used for workforce and transportation analysis. Int64 is selected because it efficiently stores large whole-number values and supports future analytical calculations.

# Why Int64 Was Chosen

The Census API returns all values as strings in the JSON response.

During the transformation process, numeric Census estimate fields are converted to Int64 because:

The official ACS documentation defines these fields as numeric estimates.
The values represent counts of people or households.
These fields will be used for aggregations, calculations, and reporting.
Int64 supports large population values without loss of precision.
Numeric datatypes improve query performance and analytical processing compared to strings.

# Column Mapping Justification

The original ACS API variables use technical column names such as `B23025_004E`, `B28002_007E`, and `B08006_013E`. These names are difficult to understand during analysis and reporting.

To improve readability while preserving the original meaning, each column was renamed based on the official ACS documentation.

The column descriptions were verified using the following Census documentation:

* B23025 Documentation:
  https://api.census.gov/data/2022/acs/acs5/groups/B23025.html

* B28002 Documentation:
  https://api.census.gov/data/2022/acs/acs5/groups/B28002.html

* B08006 Documentation:
  https://api.census.gov/data/2022/acs/acs5/groups/B08006.html

The renaming process was performed by reviewing the official variable labels in the documentation and assigning descriptive column names that accurately represent the underlying Census data.

Examples:

| Original ACS Variable | Renamed Column        |
| --------------------- | --------------------- |
| B23025_004E           | civilian_employed     |
| B23025_005E           | civilian_unemployed   |
| B28002_004E           | broadband_of_any_type |
| B28002_013E           | no_internet_access    |
| B08006_003E           | drove_alone           |
| B08006_013E           | worked_from_home      |

This approach improves data readability, simplifies downstream analysis, and maintains consistency with the official Census definitions.


# Data Cleaning Performed

1. Converted numeric estimate columns from String to Int64.
2. Preserved metro area names as String.
3. Renamed ACS variable codes to meaningful descriptive names.
4. Stored cleaned datasets as CSV and parquet files.

---

# Conclusion

The datatype assignments and column mappings are based on the official ACS documentation. String datatypes are used for descriptive geographic fields, while Int64 is used for Census estimate values and geographic identifiers because they represent numeric counts and keys.