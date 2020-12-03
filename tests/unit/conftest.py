from __future__ import absolute_import, unicode_literals

import pytest
import pytz
import uuid
from datetime import datetime, timedelta

from celery.contrib.pytest import (celery_app, celery_enable_logging,
                                   celery_parameters, depends_on_current_app,
                                   celery_config, use_celery_app_trap)
from celery.contrib.testing.app import TestApp, Trap
from django.contrib.auth import get_user_model


from django_celery_tracker.models import CeleryTask

User = get_user_model()

# Tricks flake8 into silencing redefining fixtures warnings.
__all__ = (
    'celery_app', 'celery_enable_logging', 'depends_on_current_app',
    'celery_parameters', 'celery_config', 'use_celery_app_trap'
)


@pytest.fixture(scope='session', autouse=True)
def setup_default_app_trap():
    from celery._state import set_default_app
    set_default_app(Trap())


@pytest.fixture()
def app(celery_app):
    return celery_app


@pytest.fixture(autouse=True)
def test_cases_shortcuts(request, app, patching):
    if request.instance:
        @app.task
        def add(x, y):
            return x + y

        # IMPORTANT: We set an .app attribute for every test case class.
        request.instance.app = app
        request.instance.Celery = TestApp
        request.instance.add = add
        request.instance.patching = patching
    yield
    if request.instance:
        request.instance.app = None


@pytest.fixture()
def user():
    return User.objects.create(username='user')


@pytest.fixture()
def admin():
    return User.objects.create(
        username='admin',
        is_superuser=True,
        is_staff=True
    )


START_OF_DAY = datetime(2016, 10, 8, tzinfo=pytz.utc)


@pytest.fixture()
def start_of_day():
    return START_OF_DAY


@pytest.fixture()
def test_data():
    # Entirely before
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        started=START_OF_DAY - timedelta(days=2),
        completed=START_OF_DAY - timedelta(days=2),
    )
    t.created = t.started
    t.save()

    # Starts before but ends during
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        post_state='SUCCESS',
        started=START_OF_DAY - timedelta(minutes=5),
        completed=START_OF_DAY + timedelta(minutes=5),
    )
    t.created = t.started
    t.save()

    # Starts during and ends during
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        post_state='PREMATURE_SHUTDOWN',
        started=START_OF_DAY + timedelta(hours=5),
        completed=START_OF_DAY + timedelta(hours=6),
    )
    t.created = t.started
    t.save()

    # Hasn't started yet
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
    )
    t.created = START_OF_DAY + timedelta(hours=6)
    t.save()

    # In progress
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        started=START_OF_DAY + timedelta(hours=7),
    )
    t.created = t.started
    t.save()

    # Starts during but ends after
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        post_state='FAILURE',
        started=START_OF_DAY + timedelta(days=1) - timedelta(minutes=5),
        completed=START_OF_DAY + timedelta(days=1) + timedelta(minutes=5),
    )
    t.created = t.started
    t.save()

    # Entirely after
    t = CeleryTask.objects.create(
        task_id=str(uuid.uuid4()),
        task_name='my_module.test_task',
        started=START_OF_DAY + timedelta(days=2),
        completed=START_OF_DAY + timedelta(days=2),
    )
    t.created = t.started
    t.save()
