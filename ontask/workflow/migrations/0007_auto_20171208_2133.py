# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-08 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_auto_20171125_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='Valid from',
            field=models.DateTimeField(null=True, verbose_name='Column valid from'),
        ),
        migrations.AddField(
            model_name='column',
            name='Valid until',
            field=models.DateTimeField(null=True, verbose_name='Column valid until'),
        ),
    ]