# Generated by Django 4.2.3 on 2023-12-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_linestringdata_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rasterdata',
            name='file_size',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
