# Generated by Django 4.2.3 on 2024-05-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0091_indoor'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalcategory',
            name='extra_fileds',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
