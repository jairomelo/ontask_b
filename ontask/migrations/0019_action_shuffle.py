# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0018_remove_action_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='shuffle',
            field=models.BooleanField(default=False, verbose_name='Shuffle questions?'),
        ),
    ]
