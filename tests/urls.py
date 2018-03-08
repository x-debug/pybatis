# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from pybatis.urls import urlpatterns as pybatis_urls

urlpatterns = [
    url(r'^', include(pybatis_urls, namespace='pybatis')),
]
