# Generated by Django 2.2 on 2019-04-30 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataops', '0023_pluginregistry_is_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pluginregistry',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sqlconnection',
            options={'ordering': ['name']},
        ),
    ]
