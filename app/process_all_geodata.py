from app.process_geodata import process_geodata
from .models import PolygonData, LineStringData, PointData


def process_all_geodata(df, filtered_result, standard_categories, sub_categories, categories, client, project, user, id, task_id):
    process_geodata(df, filtered_result[0], ["MultiPolygon", "Polygon"], PolygonData,
                    standard_categories, sub_categories, categories, client, project, user, id,  task_id)
    process_geodata(df, filtered_result[1], ["MultiLineString", "LineString"], LineStringData,
                    standard_categories, sub_categories, categories, client, project, user, id, task_id)
    process_geodata(df, filtered_result[2], ["MultiPoint", "Point"], PointData,
                    standard_categories, sub_categories, categories, client, project, user, id,  task_id)
    return 'Completed'
