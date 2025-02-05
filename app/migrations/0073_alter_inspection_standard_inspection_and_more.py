# Generated by Django 4.2.3 on 2024-03-04 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0072_inspectionphoto_is_inspected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='standard_inspection',
            field=models.ForeignKey(blank=True, help_text='Standard Inspection related to this inspection', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardinspection', verbose_name='Standard Inspection'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='sub_inspection',
            field=models.ForeignKey(blank=True, help_text='Sub Inspection related to this inspection', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subinspection', verbose_name='Sub Inspection'),
        ),
        migrations.AlterField(
            model_name='subinspection',
            name='standard_inspection',
            field=models.ForeignKey(blank=True, help_text='Standard Inspection related to this sub inspection', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardinspection', verbose_name='Standard Inspection'),
        ),
    ]
