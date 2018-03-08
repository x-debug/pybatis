=============================
pybatis
=============================

.. image:: https://badge.fury.io/py/pybatis.svg
    :target: https://badge.fury.io/py/pybatis

.. image:: https://travis-ci.org/x-debug/pybatis.svg?branch=master
    :target: https://travis-ci.org/x-debug/pybatis

.. image:: https://codecov.io/gh/x-debug/pybatis/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/x-debug/pybatis

python for mybatis

Documentation
-------------

The full documentation is at https://pybatis.readthedocs.io.

Quickstart
----------

Install pybatis::

    pip install pybatis

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pybatis.apps.PybatisConfig',
        ...
    )

Add pybatis's URL patterns:

.. code-block:: python

    from pybatis import urls as pybatis_urls


    urlpatterns = [
        ...
        url(r'^', include(pybatis_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
