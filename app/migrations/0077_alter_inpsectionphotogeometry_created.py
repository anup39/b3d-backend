# Generated by Django 4.2.3 on 2024-03-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0076_inpsectionphotogeometry_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inpsectionphotogeometry',
            name='created',
            field=models.BooleanField(default=False),
        ),
    ]
