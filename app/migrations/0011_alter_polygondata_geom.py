# Generated by Django 4.2.3 on 2023-10-04 09:45

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_polygondata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polygondata',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326),
        ),
    ]
