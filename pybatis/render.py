# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2016 by chenxf@partnerch.com.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
# from functools import partial
from collections import namedtuple
from django.db import connections
from django.template import Context, Template
from .const import LOADER_KEY, SQL_KEY
from .paging import paginator, QueryWrapper


class SqlExecutor:
    def __init__(self, tpl, loader, **ctx):
        self._ctx = ctx
        self._tpl = tpl
        self._loader = loader

    def _execute(self, cursor, sql, params=None):
        print('SQL:{s},PARAMS:{p}'.format(s=sql, p=params))
        params = params or list()
        return cursor.execute(sql, params)

    def _dictfetchall(self, cursor, fetch_all=True):
        columns = [col[0] for col in cursor.description]

        if fetch_all:
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        else:
            f = cursor.fetchone()
            if f:
                return dict(zip(columns, f))

    def _dictfetchall_execute(self, cursor, sql, params, fetch_all=True):
        self._execute(cursor, sql, params)
        return self._dictfetchall(cursor, fetch_all)

    def _namedtuplefetchall(self, cursor, fetch_all=True):
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])

        if fetch_all:
            return [nt_result(*row) for row in cursor.fetchall()]
        else:
            f = cursor.fetchone()
            if f:
                return nt_result(*f)

    def _namedtuplefetchall_execute(self, cursor, sql, params, fetch_all=True):
        self._execute(cursor, sql, params)
        return self._namedtuplefetchall(cursor, fetch_all)

    def _build_ctx(self, **kwargs):
        if self._loader:
            kwargs.update(**{LOADER_KEY: self._loader})
        return Context(kwargs)

    def _render_sql(self):
        ctx = self._build_ctx(**self._ctx)

        template = Template(self._tpl)
        render = template.render(ctx)
        return ctx, render

    def fetch_all(self, dict=True, using='default', cls_model=None):
        ctx, render = self._render_sql()
        if cls_model:
            dict = True
        with connections[using].cursor() as c:
            self._execute(c, render, ctx[SQL_KEY])
            if dict:
                if not cls_model:
                    return self._dictfetchall(c)
                else:
                    return [cls_model(**o) for o in self._dictfetchall(c)]
            else:
                return self._namedtuplefetchall(c)

    def fetch_one(self, dict=True, using='default', cls_model=None):
        ctx, render = self._render_sql()
        if cls_model:
            dict = True
        with connections[using].cursor() as c:
            if SQL_KEY in ctx:
                self._execute(c, render, ctx[SQL_KEY])
            else:
                self._execute(c, render)
            if dict:
                if not cls_model:
                    return self._dictfetchall(c, fetch_all=False)
                else:
                    dict_model = self._dictfetchall(c, fetch_all=False)
                    if dict_model:
                        return cls_model(**dict_model)
            else:
                return self._namedtuplefetchall(c, fetch_all=False)

    def page_dict(self, pageIndex, pageSize, using='default', **kwargs):
        return self.paging(page_no=pageIndex, per_page=pageSize, dict=True, using=using)

    def page_attr(self, pageIndex, pageSize, using='default', **kwargs):
        return self.paging(page_no=pageIndex, per_page=pageSize, dict=False, using=using)

    def page_model(self, pageIndex, pageSize, using='default', **kwargs):
        return self.paging(page_no=pageIndex, per_page=pageSize, dict=True, using=using, **kwargs)

    def paging(self, page_no=1, per_page=10, dict=True, using='default', cls_model=None, **kwargs):
        ctx, render = self._render_sql()
        with connections[using].cursor() as c:
            if cls_model:
                dict = True
            if dict:
                # func = partial(self._dictfetchall_execute, cursor=c)
                query = QueryWrapper(c, render, self._dictfetchall_execute,
                                     lambda s, p: self._dictfetchall_execute(c, s, p, fetch_all=False)['c'],
                                     ctx[SQL_KEY], using)
            else:
                # func = partial(self._namedtuplefetchall_execute, cursor=c)
                query = QueryWrapper(c, render, self._namedtuplefetchall_execute,
                                     lambda s, p: self._namedtuplefetchall_execute(c, s, p, fetch_all=False).c,
                                     ctx[SQL_KEY], using)
            return paginator(query, per_page, page_no, cls_model)

    def __str__(self):
        _, render = self._render_sql()
        return render
