# Generated by Django 4.2.3 on 2024-03-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0068_inspection_fill_color_inspection_fill_opacity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inpsectionphotogeometry',
            name='stroke_opacity',
        ),
        migrations.AddField(
            model_name='inpsectionphotogeometry',
            name='stroke_width',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
