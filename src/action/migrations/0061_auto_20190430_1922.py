# Generated by Django 2.2 on 2019-04-30 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0060_auto_20190430_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='condition',
            options={'ordering': ['-is_filter', 'name']},
        ),
    ]
