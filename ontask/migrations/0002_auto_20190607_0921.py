# Generated by Django 2.2.1 on 2019-06-06 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0001_squashed_0025_auto_20190510_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pluginregistry',
            name='is_model',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Plugin is a model'),
        ),
    ]
