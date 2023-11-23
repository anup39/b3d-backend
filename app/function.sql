
SELECT  mvt ST_AsMVT(tile, 'zxy_query_app_mill', 4096, 'geom') FROM (
    SELECT
        ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom, id 
    FROM app_mill
) AS tile WHERE geom IS NOT NULL;

