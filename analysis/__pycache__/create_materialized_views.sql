DROP MATERIALIZED VIEW IF EXISTS mv_employment_trend;
DROP MATERIALIZED VIEW IF EXISTS mv_broadband_adoption;
DROP MATERIALIZED VIEW IF EXISTS mv_remote_work_pattern;



CREATE MATERIALIZED VIEW mv_employment_trend AS
SELECT
    m.metro_area_id,
    m.metro_area_name,
    m.state_code,
    g.geo_level_name,
    d.year,
    d.period_label,
    f.emp_total AS total_population,
    f.in_labor_force,
    f.civilian_labor_force,
    f.civilian_employed,
    f.civilian_unemployed,
    f.armed_forces,
    f.not_in_labor_force,
    ROUND(f.civilian_employed::numeric / NULLIF(f.emp_total, 0) * 100, 2) AS employment_rate,
    ROUND(f.civilian_unemployed::numeric / NULLIF(f.civilian_labor_force, 0) * 100, 2) AS unemployment_rate,
    ROUND(f.in_labor_force::numeric / NULLIF(f.emp_total, 0) * 100, 2) AS labor_force_participation_rate
FROM fact_metro f
JOIN dim_metro_area m ON f.metro_area_id = m.metro_area_id
JOIN dim_date      d ON f.date_id        = d.date_id
JOIN dim_geo_level g ON f.geo_level_id   = g.geo_level_id
WHERE d.is_year_start = true
ORDER BY m.state_code, d.year;

CREATE INDEX idx_mv_emp_state ON mv_employment_trend(state_code);
CREATE INDEX idx_mv_emp_year  ON mv_employment_trend(year);



CREATE MATERIALIZED VIEW mv_broadband_adoption AS
SELECT
    m.metro_area_id,
    m.metro_area_name,
    m.state_code,
    g.geo_level_name,
    d.year,
    d.period_label,
    f.brd_total AS total_households,
    f.with_internet_subscription,
    f.broadband_of_any_type,
    f.cellular_data_plan,
    f.cellular_data_plan_only,
    f.broadband_cable_fiber_or_dsl,
    f.broadband_cable_fiber_or_dsl_only,
    f.satellite_internet_service,
    f.satellite_internet_service_only,
    f.no_internet_access,
    f.internet_access_without_subscription,
    ROUND(f.broadband_of_any_type::numeric / NULLIF(f.brd_total, 0) * 100, 2) AS broadband_adoption_rate,
    ROUND(f.no_internet_access::numeric / NULLIF(f.brd_total, 0) * 100, 2) AS no_internet_rate,
    ROUND(f.cellular_data_plan::numeric / NULLIF(f.brd_total, 0) * 100, 2) AS cellular_adoption_rate,
    ROUND(f.broadband_cable_fiber_or_dsl::numeric / NULLIF(f.brd_total, 0) * 100, 2) AS cable_fiber_dsl_rate
FROM fact_metro f
JOIN dim_metro_area m ON f.metro_area_id = m.metro_area_id
JOIN dim_date      d ON f.date_id        = d.date_id
JOIN dim_geo_level g ON f.geo_level_id   = g.geo_level_id
WHERE d.is_year_start = true
ORDER BY m.state_code, d.year;

CREATE INDEX idx_mv_brd_state ON mv_broadband_adoption(state_code);
CREATE INDEX idx_mv_brd_year  ON mv_broadband_adoption(year);



CREATE MATERIALIZED VIEW mv_remote_work_pattern AS
SELECT
    m.metro_area_id,
    m.metro_area_name,
    m.state_code,
    g.geo_level_name,
    d.year,
    d.period_label,
    f.total_workers,
    f.car_truck_or_van,
    f.drove_alone,
    f.carpooled,
    f.public_transportation,
    f.bus,
    f.worked_from_home,
    f.walked,
    f.bicycle,
    f.motorcycle,
    f.taxicab,
    ROUND(f.worked_from_home::numeric / NULLIF(f.total_workers, 0) * 100, 2) AS wfh_rate,
    ROUND(f.drove_alone::numeric / NULLIF(f.total_workers, 0) * 100, 2) AS drove_alone_rate,
    ROUND(f.public_transportation::numeric / NULLIF(f.total_workers, 0) * 100, 2) AS public_transport_rate,
    ROUND(f.carpooled::numeric / NULLIF(f.total_workers, 0) * 100, 2) AS carpool_rate
FROM fact_metro f
JOIN dim_metro_area m ON f.metro_area_id = m.metro_area_id
JOIN dim_date      d ON f.date_id        = d.date_id
JOIN dim_geo_level g ON f.geo_level_id   = g.geo_level_id
WHERE d.is_year_start = true
ORDER BY m.state_code, d.year;

CREATE INDEX idx_mv_wfh_state ON mv_remote_work_pattern(state_code);
CREATE INDEX idx_mv_wfh_year  ON mv_remote_work_pattern(year);

SELECT matviewname FROM pg_matviews WHERE schemaname = 'public';