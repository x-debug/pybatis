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
from .render import SqlExecutor
from .const import _SQL_ENGINE_MYSQL, OFF_AUTO_ESCAPE_BEGIN, OFF_AUTO_ESCAPE_END

try:
    loader_path = settings.SQL_TEMPLATES
except Exception:
    loader_path = os.path.join(settings.BASE_DIR, 'sql_templates')

try:
    db_settings = settings.DATABASES
except:
    db_settings = {}


def _get_db_context(db_ctx):
    return dict(
        zip(db_ctx.keys(), [e['NAME'] for e in db_ctx.values() if e['ENGINE'] == _SQL_ENGINE_MYSQL] or ['main']))


db_dict = _get_db_context(db_settings)


class SqlStatementLoader:
    def __init__(self, ext='.html'):
        self._cache_loaders = {}
        self._ext = ext

    @property
    def file_ext(self):
        return self._ext

    class InnerLoader:
        def __init__(self, module, container):
            self._module = module
            self._container = container

        @property
        def container(self):
            return self._container

        @property
        def module(self):
            return self._module

        def __getattr__(self, item):
            def load_templates(**kwargs):
                file_path = os.path.join(loader_path, self._module + self._container.file_ext)
                # TODO 需要优化该载入方式
                with open(file=file_path, encoding='utf8', mode='rt') as tpl:
                    stream = tpl.read()
                    _ = pq(stream)
                    kwargs.update(**db_dict)
                    return SqlExecutor(''.join([OFF_AUTO_ESCAPE_BEGIN, _('sql#' + item).text(), OFF_AUTO_ESCAPE_END]),
                                       self, **kwargs)

            return load_templates

    def __getattr__(self, item):
        if item in self._cache_loaders:
            return self._cache_loaders.get(item)
        else:
            loader = self.InnerLoader(item, self)
            self._cache_loaders[item] = loader
            return loader


statement_loader = SqlStatementLoader()
