=========================
Celery Tracker for Django
=========================

|build-status| |coverage|

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

Release
=======
switch to ``master`` branch:
----------------------------
- Change package version in ``django_celery_tracker/__init__.py`` according to release changes (``major|minor|patch``).
- Update ``CHANGELOG.md``:
  - Rename ``[Unreleased]`` section to reflect new release version and release date, same format as for all previous releases
  - Create new ``[Unreleased]`` section on top of file, as it was previously
  - On the bottom of ``CHANGELOG.md`` file, create comparison reference for current release changes:

.. code-block:: md

    # was
    [Unreleased]: https://github.com/chris-allen/django-celery-tracker/compare/v0.3.0...HEAD
    [0.3.0]: https://github.com/chris-allen/django-celery-tracker/compare/v0.2.0...v0.3.0

    # became
    # - "Unreleased" renamed to commit version
    # - new "Unreleased" created, comparing last "0.4.0" commit with "HEAD"
    [Unreleased]: https://github.com/chris-allen/django-celery-tracker/compare/v0.4.0...HEAD
    [0.4.0]: https://github.com/chris-allen/django-celery-tracker/compare/v0.3.0...v0.4.0
    [0.3.0]: https://github.com/chris-allen/django-celery-tracker/compare/v0.2.0...v0.3.0

- Commit ``CHANGELOG.md`` and ``django_celery_tracker/__init__.py`` with message ``:rocket: {version}`` (where version is your release version)

.. |build-status| image:: https://travis-ci.com/chris-allen/django-celery-tracker.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.com/chris-allen/django-celery-tracker

.. |coverage| image:: https://codecov.io/gh/chris-allen/django-celery-tracker/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/chris-allen/django-celery-tracker?branch=master
