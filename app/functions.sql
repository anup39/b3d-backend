CREATE OR REPLACE FUNCTION function_zxy_query_app_polygondata_by_project_category(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    project text;
    category text;
BEGIN
    project := trim((query_params::jsonb) ->> 'project');
    category := trim((query_params::jsonb) ->> 'category');

    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_polygondata_by_project_category', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom, id , project_id ,category_id
        FROM app_polygondata 
        WHERE  project_id::text = project AND category_id::text = category
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END;
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_polygondata_by_project_category IS 'Filters the Polygon table by project and category';


CREATE OR REPLACE FUNCTION function_zxy_query_app_polygondata_by_project(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    project text;
BEGIN
    project := trim((query_params::jsonb) ->> 'project');
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_polygondata_by_project', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom, id , project_id ,category_id
        FROM app_polygondata 
        WHERE  project_id::text = project 
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END;
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_polygondata_by_project IS 'Filters the Polygon table by project';