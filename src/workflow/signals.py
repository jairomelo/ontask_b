# -*- coding: utf-8 -*-

from django.db.models.signals import post_delete
from django.dispatch import receiver

import logging
from . import models
from workflow.models import Workflow
from dataops import pandas_db

logger = logging.getLogger("project")

@receiver(post_delete, sender=Workflow)
def delete_data_frame_table(sender, instance, **kwargs):
    if instance.has_table():
        pandas_db.delete_table(instance.get_data_frame_table_name())