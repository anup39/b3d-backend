# Generated by Django 4.2.3 on 2023-11-11 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_category_client_categorystyle_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardcategory',
            name='client',
            field=models.ForeignKey(help_text='Client Associated with this', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.client', verbose_name='Client'),
        ),
    ]
