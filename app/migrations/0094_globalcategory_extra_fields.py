# Generated by Django 4.2.3 on 2024-05-20 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0093_remove_globalcategory_extra_fileds'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalcategory',
            name='extra_fields',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
