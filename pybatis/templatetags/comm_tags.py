# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2016 by chenxf@partnerch.com.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import os
from django.conf import settings
from pyquery import PyQuery as pq
from pybatis.loader import statement_loader
from pybatis.const import LOADER_KEY, SQL_KEY

try:
    loader_path = settings.SQL_TEMPLATES
except Exception:
    loader_path = os.path.join(settings.BASE_DIR, 'sql_templates')
from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name='safe')
def do_safe(context, value):
    if SQL_KEY not in context:
        context[SQL_KEY] = list()
    context[SQL_KEY].append(value)
    return '%s'


@register.filter(name='like')
def do_like(value, middle=0):
    if middle == 0:
        return '%' + value + '%'
    elif middle == -1:
        return '%' + value
    elif middle == 1:
        return value + '%'


@register.simple_tag(takes_context=True, name='include_block')
def do_include_block(context, value):
    if SQL_KEY not in context:
        context[SQL_KEY] = list()
    if '.' in value:
        module_, function_ = value.split('.')
    else:
        loader = context[LOADER_KEY]
        module_ = loader.module
        function_ = value
    render_func = getattr(getattr(statement_loader, module_), function_)
    return str(render_func(**context.dicts[-1])).strip()
