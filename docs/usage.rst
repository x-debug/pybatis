=====
Usage
=====

To use pybatis in a project, add it to your `INSTALLED_APPS`:

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
