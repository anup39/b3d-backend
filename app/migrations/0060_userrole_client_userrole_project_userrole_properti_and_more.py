# Generated by Django 4.2.3 on 2023-11-11 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_alter_rasterdata_options_category_properti_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='client',
            field=models.ForeignKey(help_text='Client Associated with this', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.client', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='project',
            field=models.ForeignKey(help_text='Project', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_as_user', to='app.project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='properti',
            field=models.ForeignKey(help_text='User related to this property', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.rasterdata', verbose_name='Property'),
        ),
        migrations.DeleteModel(
            name='UserProject',
        ),
    ]
