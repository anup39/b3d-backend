# Generated by Django 4.2.3 on 2024-03-02 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_inspectionreport_inspectionphoto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='project',
            field=models.ForeignKey(help_text='Project related to this inspection', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
    ]
