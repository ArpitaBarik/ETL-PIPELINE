DROP TABLE IF EXISTS mart_employment;
DROP TABLE IF EXISTS mart_broadband;
DROP TABLE IF EXISTS mart_commute;



CREATE TABLE mart_employment AS
SELECT
    metro_area_id,
    metro_area_name,
    state_code,
    geo_level_name,
    year,
    period_label,

    -- Raw counts
    total_population,
    in_labor_force,
    civilian_labor_force,
    civilian_employed,
    civilian_unemployed,
    armed_forces,
    not_in_labor_force,

    -- Calculated rates
    employment_rate,
    unemployment_rate,
    labor_force_participation_rate

FROM mv_employment_trend
ORDER BY state_code, year;

-- Add primary key
ALTER TABLE mart_employment
ADD CONSTRAINT pk_mart_employment
PRIMARY KEY (metro_area_id, year);

-- Add indexes for fast filtering
CREATE INDEX idx_mart_emp_state  ON mart_employment(state_code);
CREATE INDEX idx_mart_emp_year   ON mart_employment(year);
CREATE INDEX idx_mart_emp_period ON mart_employment(period_label);

SELECT 'mart_employment created — ' || COUNT(*) || ' rows' AS status
FROM mart_employment;


CREATE TABLE mart_broadband AS
SELECT
    metro_area_id,
    metro_area_name,
    state_code,
    geo_level_name,
    year,
    period_label,

    -- Raw counts
    total_households,
    with_internet_subscription,
    broadband_of_any_type,
    cellular_data_plan,
    cellular_data_plan_only,
    broadband_cable_fiber_or_dsl,
    broadband_cable_fiber_or_dsl_only,
    satellite_internet_service,
    satellite_internet_service_only,
    no_internet_access,
    internet_access_without_subscription,

    -- Calculated rates
    broadband_adoption_rate,
    no_internet_rate,
    cellular_adoption_rate,
    cable_fiber_dsl_rate

FROM mv_broadband_adoption
ORDER BY state_code, year;

-- Add primary key
ALTER TABLE mart_broadband
ADD CONSTRAINT pk_mart_broadband
PRIMARY KEY (metro_area_id, year);

-- Add indexes
CREATE INDEX idx_mart_brd_state  ON mart_broadband(state_code);
CREATE INDEX idx_mart_brd_year   ON mart_broadband(year);
CREATE INDEX idx_mart_brd_period ON mart_broadband(period_label);

SELECT 'mart_broadband created — ' || COUNT(*) || ' rows' AS status
FROM mart_broadband;


CREATE TABLE mart_commute AS
SELECT
    metro_area_id,
    metro_area_name,
    state_code,
    geo_level_name,
    year,
    period_label,

    -- Raw counts
    total_workers,
    car_truck_or_van,
    drove_alone,
    carpooled,
    public_transportation,
    bus,
    worked_from_home,
    walked,
    bicycle,
    motorcycle,
    taxicab,

    -- Calculated rates
    wfh_rate,
    drove_alone_rate,
    public_transport_rate,
    carpool_rate

FROM mv_remote_work_pattern
ORDER BY state_code, year;

-- Add primary key
ALTER TABLE mart_commute
ADD CONSTRAINT pk_mart_commute
PRIMARY KEY (metro_area_id, year);

-- Add indexes
CREATE INDEX idx_mart_com_state  ON mart_commute(state_code);
CREATE INDEX idx_mart_com_year   ON mart_commute(year);
CREATE INDEX idx_mart_com_period ON mart_commute(period_label);

SELECT 'mart_commute created — ' || COUNT(*) || ' rows' AS status
FROM mart_commute;

-- STEP 5 — VALIDATE ALL 3 MART TABLES

-- Check 1: Row counts
SELECT 'mart_employment' AS mart_name, COUNT(*) AS rows FROM mart_employment
UNION ALL
SELECT 'mart_broadband'  AS mart_name, COUNT(*) AS rows FROM mart_broadband
UNION ALL
SELECT 'mart_commute'    AS mart_name, COUNT(*) AS rows FROM mart_commute;

-- Check 2: All 3 years present
SELECT year, COUNT(*) AS metro_count
FROM mart_employment
GROUP BY year
ORDER BY year;

-- Check 3: No null rates in employment mart
SELECT COUNT(*) AS null_unemployment_rates
FROM mart_employment
WHERE unemployment_rate IS NULL;

-- Check 4: No null rates in broadband mart
SELECT COUNT(*) AS null_broadband_rates
FROM mart_broadband
WHERE broadband_adoption_rate IS NULL;

-- Check 5: No null rates in commute mart
SELECT COUNT(*) AS null_wfh_rates
FROM mart_commute
WHERE wfh_rate IS NULL;