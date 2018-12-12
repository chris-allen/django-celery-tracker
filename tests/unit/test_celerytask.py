from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
from itertools import count
from time import time

import pytest

from celery import states
# from celery.events import Event as _Event
from celery.events.state import State, Worker, Task
from celery.utils import gen_unique_id

# from django.test.utils import override_settings
# from django.utils import timezone

from celery_tracker.models import CeleryTask

_ids = count(0)

@pytest.mark.django_db()
@pytest.mark.usefixtures('depends_on_current_app')
class test_CeleryTask:

    def create_task(self, worker, **kwargs):
        d = dict(uuid=gen_unique_id(),
                 name='django_celery_tracker.test.task{0}'.format(next(_ids)),
                 worker=worker)
        return Task(**dict(d, **kwargs))

    @pytest.fixture(autouse=True)
    def setup_app(self, app):
        self.app = app

    def test_constructor(self):
        cam = CeleryTask()
        assert cam

    def test_handle_task_received(self):
        worker = Worker(hostname='fuzzie')
        worker.event('online', time(), time(), {})
        # self.cam.handle_worker((worker.hostname, worker))

        task = self.create_task(worker)
        task.event('received', time(), time(), {})
        assert task.state == states.RECEIVED