=========================
Celery Tracker for Django
=========================

|build-status|

This django extension is intended for existing celery projects that want better monitoring of what's going on in their queue.

Usage
=====

To use this with your project, you need to:

1. Install django-celery-tracker:

.. code-block:: console

    $ pip install django-celery-tracker

1. Add ``django_celery_tracker`` to ``INSTALLED_APPS`` in your Django settings file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_celery_tracker',
    )

1. Create the database tables by applying migrations:

.. code-block:: console

    $ python manage.py migrate django_celery_tracker

1. You will now have a record of all *future* celery tasks and their progress which can be queried like so:

.. code-block:: console

    $ python manage.py console
    ...
    >>> from django_celery_tracker.models import CeleryTask
    >>> CeleryTask.objects.all()
    <QuerySet [<CeleryTask: id=3d889396-daa2-4209-9348-9ec71bfb1262, name=api.taskapp.celery.debug_task>]

Dashboard
=========

Optionally, you can include a dashboard view that can only be accessed by admin users. To add the dashboard to your project, simply add the following to your ``urls.py``:

.. code-block:: python

    urlpatterns = [
        path("celery-tracker/", include("django_celery_tracker.urls")),
    ]

You can now visit ``http://site_url/celery-tracker`` to view the status of your tasks!

Disclaimer
==========

The datastore for a celery message queue is usually in-memory and highly-optimized (eg ``redis`` or ``rabbitmq``).  This django extension creates a database entry for every celery task that is created. You may want to periodically delete older entries if storage is an obstacle.

.. |build-status| image:: https://github.com/chris-allen/django-celery-tracker/actions/workflows/static_tests.yml/badge.svg
    :alt: Build status
    :target: https://github.com/chris-allen/django-celery-tracker/actions/workflows/static_tests.yml
