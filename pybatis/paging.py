# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) 2016 by chenxf@partnerch.com.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from django.core.paginator import Paginator


def paginator(data_list, per_page, page_no, cls_model=None):
    """封装Django分页"""
    pages = Paginator(data_list, per_page)

    # 防止超出页数
    if not page_no > 0:
        page_no = 1
    if page_no > pages.num_pages:
        page_no = pages.num_pages

    p = pages.page(page_no)  # 获取本页数据

    data = dict()  # 获取分页信息
    data['count'] = pages.count
    data['page_num'] = pages.num_pages
    data['per_page'] = per_page
    data['current'] = page_no
    data['start_index'] = p.start_index() - 1
    if not cls_model:
        return p.object_list, page_no, data
    else:
        return [cls_model(**o) for o in p.object_list], page_no, data


class QueryWrapper(object):
    """查询集包装器。实现django Paginator需要的必要方法，实现和query一样使用Paginator分页"""

    def __init__(self, cursor, sql, cb, ncb, params=None, db="default"):
        """
        :param sql: sql语句
        :param params: sql语句的params参数
        :param db: 数据库名称（Django配置）
        """
        self.cursor = cursor
        self.db = db
        self.sql = sql
        self.params = params
        self.cb = cb
        self.ncb = ncb

    def count(self):
        """计算总页数"""

        sql = """SELECT COUNT(*) AS c FROM (%s) _count""" % self.sql
        return self.ncb(sql, self.params)  # 返回总页数

    def __len__(self):
        return self.count()

    def __getitem__(self, item):
        """ self.__getslice(x, y) = self[x:y]"""
        x, y = item.start, item.stop
        sql = self.sql + ' LIMIT {start}, {num}'.format(start=x, num=y - x)
        return self.cb(self.cursor, sql, self.params)  # 字典列表形式返回
