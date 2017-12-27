# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.conf.urls import url

import dataops.upload
from . import views
from . import csvupload, excelupload, sqlupload
from . import plugin_manager

app_name = 'dataops'

urlpatterns = [

    url(r'^$', views.dataops, name="list"),

    url(r'^uploadmerge/$', views.uploadmerge, name="uploadmerge"),

    url(r'^transform/$', views.transform, name="transform"),

    # Manual Data Entry
    url(r'^rowupdate/$', views.row_update, name="rowupdate"),

    url(r'^rowcreate/$', views.row_create, name="rowcreate"),

    # CSV Upload/Merge
    url(r'^csvupload1/$', csvupload.csvupload1, name='csvupload1'),

    # Excel Upload/Merge
    url(r'^excelupload1/$', excelupload.excelupload1, name='excelupload1'),

    # Excel Upload/Merge
    url(r'^sqlupload1/$', sqlupload.sqlupload1, name='sqlupload1'),

    # Upload/Merge
    url(r'^upload_s2/$', dataops.upload.upload_s2, name='upload_s2'),

    url(r'^upload_s3/$', dataops.upload.upload_s3, name='upload_s3'),

    url(r'^upload_s4/$', dataops.upload.upload_s4, name='upload_s4'),

    url(r'^(?P<pk>\d+)/plugin_invoke/$', plugin_manager.run,
        name='plugin_invoke'),
]
