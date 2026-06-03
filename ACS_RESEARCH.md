# ACS Census Table Research (Employment, Broadband, Commute)

## Objective

The goal was to identify appropriate American Community Survey (ACS) tables that can be accessed through the Census API and used for state-level and metropolitan-level analysis.

The required topics were:

* Employment
* Broadband / Internet usage
* Commute patterns (Transportation to work)

---

## Research Method

I used the official Census API documentation.
First, I searched the groups list to identify all available tables related to each topic.
I noticed that each topic had many tables, not just one.

Therefore, I needed a rule to identify the core dataset.

---

I selected tables based on the following criteria:

1. The table must represent the **entire population**.
2. The title must be general and not filtered by race, age, disability, or income.
3. The table must contain a total value and main categories.
4. The table must be accessible via the Census API for both state and metropolitan geography.

I rejected tables that contained:

* "by age"
* "by race"
* "by disability"
* "by education"
* "workplace geography"
  because those represent subgroup analysis, not baseline indicators.

---

## Selected Tables

### 1. Employment

**Table:** B23025 — Employment Status (Population 16 years and over)

Reason:
This table provides labor force participation, employed, and unemployed counts for the general population.
Other employment tables were subgroup studies (e.g., disability or grandparents) and were not suitable.

**Selected Variables:**

* B23025_001E  Total
* B23025_002E  In labor force
* B23025_003E  Civilian labor force
* B23025_004E  Employed
* B23025_005E  Unemployed
* B23025_006E  Armed forces
* B23025_007E  Not in labor force

---

### 2. Broadband / Internet Usage

**Table:** B28002 — Presence and Types of Internet Subscriptions in Household

Reason:
This table measures household internet access and broadband adoption.
Other tables (like computer ownership or subject tables) were not direct broadband indicators.

**Selected Variables:**

* B28002_001E  Total households                  
* B28002_002E  With an internet subscription    
* B28002_003E  Dial-up internet only             
* B28002_004E  Broadband such as cable/fiber/DSL 
* B28002_005E  Cellular data plan only           
* B28002_006E  Satellite internet service        
* B28002_007E  Multiple internet types           
* B28002_008E  Broadband + cellular              
* B28002_009E  Broadband + satellite             
* B28002_010E  Cellular + satellite              
* B28002_011E  Cellular + satellite + broadband  
* B28002_012E  Other internet service            
*  B28002_013E  No internet access                

---

### 3. Commute Patterns

**Table:** B08006 — Means of Transportation to Work

Reason:
This table provides transportation mode for workers and is a standard commuting dataset.
Tables filtered by race or workplace geography were rejected.

**Selected Variables:**
* B08006_001E	Total workers
* B08006_002E	Car, truck, or van
* B08006_003E	Drove alone
* B08006_004E	Carpooled
* B08006_005E	Public transportation (overall)
* B08006_006E	Bus
* B08006_007E	Subway or elevated rail
* B08006_008E	Railroad
* B08006_009E	Ferryboat
* B08006_010E	Taxicab
* B08006_011E	Motorcycle
* B08006_012E	Bicycle
* B08006_013E	Walked
* B08006_014E	Other means
* B08006_015E	Worked from home  upto B08006_050E 
---