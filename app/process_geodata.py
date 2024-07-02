import time
from django.contrib.gis.geos import GEOSGeometry
from .models import Category, MeasuringFileUpload
# from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon
from shapely.geometry import Polygon, MultiPolygon, Point , LineString , MultiLineString


def convert_3D_2D(geometry):
    '''
    Takes a 3D geometry (has_z) and returns a 2D geometry
    '''
    print (geometry,'geometry')
    if geometry.has_z:
        print(geometry.has_z, 'geometry.has_z')
        print(geometry.geom_type, 'geometry.geom_type')
        if geometry.geom_type == 'Point':
            return Point(geometry.x, geometry.y)
        elif geometry.geom_type == 'MultiPoint':
            return MultiPoint([(x, y) for x, y, _ in geometry.coords])
        elif geometry.geom_type == 'LineString':
            return LineString([(x, y) for x, y, _ in geometry.coords])
        elif geometry.geom_type == 'MultiLineString':
            new_multi_l = []
            for l in geometry:
                new_multi_l.append(LineString([(x, y) for x, y, _ in l.coords]))
            return MultiLineString(new_multi_l)
        elif geometry.geom_type == 'Polygon':
            lines = [xy[:2] for xy in list(geometry.exterior.coords)]
            return Polygon(lines)
        elif geometry.geom_type == 'MultiPolygon':
            new_multi_p = []
            for p in geometry:
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_multi_p.append(Polygon(lines))
            return MultiPolygon(new_multi_p)
    else:
        return geometry

def process_geodata(df, filtered_result, geom_type, DataModel, standard_categories, sub_categories, categories, client, project, user, id, task_id):
    print(id, 'id')
    print(task_id, 'task_id')
    measuring_upload = MeasuringFileUpload.objects.get(id=id)
    names_to_filter = [item.get('cleaned_name') for item in filtered_result]
    gdf = df[df['cleaned_name'].isin(names_to_filter)].copy()
    if len(gdf) > 0:
        measuring_upload.status = 'Uploading'
        measuring_upload.save()
        gdf.loc[:, 'project'] = project.id
        gdf.loc[:, 'client'] = client.id
        gdf.loc[:, 'client'] = gdf['client'].astype('Int64')
        gdf.loc[:, 'project'] = gdf['project'].astype('Int64')
        gdf = gdf.loc[gdf.geometry.type.isin(geom_type)]

        print(len(gdf), f'length of gdf_{geom_type[0]} after reset index')

        def create_category(name):
            for i in filtered_result:
                if i.get('cleaned_name') == name:
                    return i.get('matched_category')

        gdf.loc[:, 'category'] = gdf.apply(
            lambda row: create_category(row['cleaned_name']), axis=1)
        gdf.loc[:, 'category'] = gdf['category'].astype('Int64')
        gdf.loc[:, 'standard_category'] = gdf['category'].map(
            lambda x: Category.objects.get(id=x).standard_category.id)
        gdf.loc[:, 'standard_category'] = gdf['standard_category'].astype(
            'Int64')
        gdf.loc[:, 'sub_category'] = gdf['category'].map(
            lambda x: Category.objects.get(id=x).sub_category.id)
        gdf.loc[:, 'sub_category'] = gdf['sub_category'].astype('Int64')
        gdf.loc[:, 'standard_category_name'] = gdf['category'].map(
            lambda x: Category.objects.get(id=x).standard_category.name)
        gdf.loc[:, 'sub_category_name'] = gdf['category'].map(
            lambda x: Category.objects.get(id=x).sub_category.name)
        gdf.loc[:, 'category_name'] = gdf['category'].map(
            lambda x: Category.objects.get(id=x).name)
        gdf.loc[:, 'created_by'] = user.id
        gdf.loc[:, 'is_display'] = True

        print(gdf[['project', 'client', 'standard_category', 'sub_category', 'category',
                   'standard_category_name', 'sub_category_name', 'category_name', 'created_by', 'is_display']].head(15))
        print(len(gdf), f'length of gdf_{geom_type[0]}')
        gdf = gdf.explode(ignore_index=True)
        print(len(gdf), f'length of gdf_{geom_type[0]} after explode')

        start_time = time.time()
        data_list = [
            DataModel(
                client=client,
                project=project,
                standard_category=standard_categories[row['standard_category']],
                sub_category=sub_categories[row['sub_category']],
                category=categories[row['category']],
                standard_category_name=standard_categories[row['standard_category']].name,
                sub_category_name=sub_categories[row['sub_category']].name,
                category_name=categories[row['category']].name,
                geom=GEOSGeometry(convert_3D_2D(row['geometry']).wkt),
                created_by=user,
                is_display=row['is_display'],
                task_id=task_id,
            )
            for _, row in gdf.iterrows()
        ]

        DataModel.objects.bulk_create(data_list)
        end_time = time.time()
        execution_time = end_time - start_time
        measuring_upload.progress = 33
        print(
            f'Time taken to upload {geom_type[0]} {len(gdf)} the code: {execution_time} seconds')
