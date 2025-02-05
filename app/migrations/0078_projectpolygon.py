# Generated by Django 4.2.3 on 2024-03-14 10:06

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0077_alter_inpsectionphotogeometry_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPolygon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('attributes', models.JSONField(default=dict, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_display', models.BooleanField(default=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(help_text='The person who created the polygon', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('project', models.ForeignKey(help_text='Project Associated with this polygon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project')),
            ],
            options={
                'verbose_name_plural': 'ProjectPolygon',
            },
        ),
    ]
