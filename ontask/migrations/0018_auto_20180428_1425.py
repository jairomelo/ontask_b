# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 04:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0017_auto_20180417_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ('-is_key',)},
        ),
    ]
