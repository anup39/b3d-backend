# Generated by Django 4.2.3 on 2023-11-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_project_options_userproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='linestringdata',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='linestringdata',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pointdata',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pointdata',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='polygondata',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='polygondata',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='is_display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
    ]
