from __future__ import absolute_import, unicode_literals

from itertools import count
import pytest

from django_celery_tracker.models import CeleryTask
from django_celery_tracker.signals import (
    task_publish_handler,
    task_prerun_handler,
    task_postrun_handler,
)

_ids = count(0)


@pytest.mark.django_db()
@pytest.mark.usefixtures('depends_on_current_app')
class test_CeleryTask:

    @pytest.fixture(autouse=True)
    def setup_app(self, app):
        self.app = app

    def test_constructor(self):
        task_id = 'task-{0}'.format(next(_ids))
        task = CeleryTask(
            task_id=task_id,
            task_name='django_celery_tracker.test.task',
        )

        assert task
        assert str(task) == 'id={0}, name={1}'.format(
            task_id, 'django_celery_tracker.test.task',
        )

    def test_worker_success(self):
        headers = {
            'id': 'task-{0}'.format(next(_ids)),
            'task': 'django_celery_tracker.test.task',
            'argsrepr': '(1,)',
        }
        task_publish_handler(headers=headers)

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=True,
            completed__isnull=True,
        ).exists()

        task_prerun_handler(task_id=headers['id'])

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=False,
            completed__isnull=True,
        ).exists()

        task_postrun_handler(task_id=headers['id'], state='SUCCESS')

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=False,
            completed__isnull=False,
            post_state='SUCCESS',
        ).exists()

    def test_worker_failure(self):
        headers = {
            'id': 'task-{0}'.format(next(_ids)),
            'task': 'django_celery_tracker.test.task',
            'argsrepr': '(1,)',
        }
        task_publish_handler(headers=headers)

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=True,
            completed__isnull=True,
        ).exists()

        task_prerun_handler(task_id=headers['id'])

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=False,
            completed__isnull=True,
        ).exists()

        task_postrun_handler(task_id=headers['id'])

        assert CeleryTask.objects.filter(
            task_id=headers['id'],
            created__isnull=False,
            started__isnull=False,
            completed__isnull=False,
            post_state='PREMATURE_SHUTDOWN',
        ).exists()
