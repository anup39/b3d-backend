import time
from django.contrib.gis.geos import GEOSGeometry
from .models import Category, PolygonData, LineStringData, PointData


def process_geodata(df, filtered_result, geom_type, DataModel, request, standard_categories, sub_categories, categories, client, project, user, id, task_id):
    print(id, 'id')
    print(task_id, 'task_id')
    names_to_filter = [item.get('cleaned_name') for item in filtered_result]
    gdf = df[df['cleaned_name'].isin(names_to_filter)].copy()
    if len(gdf) > 0:
        gdf.loc[:, 'project'] = request.data.get('project_id')
        gdf.loc[:, 'client'] = request.data.get('client_id')
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
        gdf.loc[:, 'created_by'] = request.data.get('user_id')
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
                geom=GEOSGeometry(row['geometry'].wkt),
                created_by=user,
                is_display=row['is_display'],
                task_id=task_id,
            )
            for _, row in gdf.iterrows()
        ]

        # DataModel.objects.bulk_create(data_list)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f'Time taken to upload {geom_type[0]} {len(gdf)} the code: {execution_time} seconds')
