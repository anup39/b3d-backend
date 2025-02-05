# Generated by Django 4.2.3 on 2023-12-25 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_alter_rasterdata_file_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='OBJData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('obj_file', models.FileField(upload_to='Uploads/OBJData')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_display', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_edited', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'OBJData',
            },
        ),
    ]
