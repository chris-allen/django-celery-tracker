from __future__ import absolute_import, unicode_literals

import pytest
import uuid
import json
from unittest.mock import patch, PropertyMock
from urllib.parse import quote_plus
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.template.response import HttpResponse, SimpleTemplateResponse
from django.urls import resolve

from django_celery_tracker.models import CeleryTask
from django_celery_tracker.views import (
    tracker_dashboard,
    timeline_page_data,
    task_details,
)

User = get_user_model()


@pytest.mark.django_db()
class test_Dashboard:

    def test_root_url_is_dashboard_view(self):
        found = resolve('/celery-tracker/')
        assert found.func == tracker_dashboard

    def test_timeline_url_is_timeline_view(self):
        found = resolve('/celery-tracker/timeline-data/')
        assert found.func == timeline_page_data

    def test_details_url_is_details_view(self):
        found = resolve("/celery-tracker/task-details/%s/" % str(uuid.uuid4()))
        assert found.func == task_details

    def test_dashboard_creds(self, client, user, admin):
        # Try URL without any creds
        response = client.get('/celery-tracker/')

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == '/admin/login/?next=/celery-tracker/'

        # Try URL with non-superuser creds
        client.force_login(user)
        response = client.get('/celery-tracker/')

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == '/admin/login/?next=/celery-tracker/'

        # Try URL with superuser creds
        client.force_login(admin)
        response = client.get('/celery-tracker/')

        assert isinstance(response, SimpleTemplateResponse)

    def test_timeline_creds(self, client, user, admin):
        # Try URL without any creds
        response = client.get('/celery-tracker/timeline-data/')

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == (
            '/admin/login/?next=/celery-tracker/timeline-data/'
        )

        # Try URL with non-superuser creds
        client.force_login(user)
        response = client.get('/celery-tracker/timeline-data/')

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == (
            '/admin/login/?next=/celery-tracker/timeline-data/'
        )

        # Try URL with superuser creds
        client.force_login(admin)
        response = client.get('/celery-tracker/timeline-data/')

        assert isinstance(response, HttpResponse)
        assert response.status_code == 400

    def test_task_details_creds(self, client, user, admin):
        dummy_uuid = str(uuid.uuid4())

        # Try URL without any creds
        response = client.get('/celery-tracker/task-details/%s/' % dummy_uuid)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == (
            '/admin/login/?next=/celery-tracker/task-details/%s/' % dummy_uuid
        )

        # Try URL with non-superuser creds
        client.force_login(user)
        response = client.get('/celery-tracker/task-details/%s/' % dummy_uuid)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == (
            '/admin/login/?next=/celery-tracker/task-details/%s/' % dummy_uuid
        )

        # Try URL with superuser creds
        client.force_login(admin)
        response = client.get('/celery-tracker/task-details/%s/' % dummy_uuid)

        assert isinstance(response, HttpResponse)
        assert response.status_code == 404

    def test_timeline_filtering(self, admin_client, start_of_day, test_data):
        date = quote_plus(str(start_of_day))

        # Validate 7 entries exist
        assert CeleryTask.objects.all().count() == 7

        # Only 5 happen on the day
        response = admin_client.get(
            '/celery-tracker/timeline-data/?date=' + date
        )
        response_arr = json.loads(response.content.decode("utf-8"))

        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        assert len(response_arr) == 5

    @patch("django_celery_tracker.views.AsyncResult")
    def test_task_details(self,
                          mock_AsyncResult,
                          admin_client,
                          start_of_day,
                          test_data):
        date = quote_plus(str(start_of_day))

        response = admin_client.get(
            '/celery-tracker/timeline-data/?date=' + date
        )
        response_arr = json.loads(response.content.decode("utf-8"))

        for idx, task in enumerate(response_arr):
            # Init to be empty object
            mock_AsyncResult.return_value = type('', (), {})()

            # Simulate task model without result
            if idx == 0:
                type(mock_AsyncResult.return_value).state = (
                    PropertyMock(side_effect=TypeError)
                )
            else:
                mock_AsyncResult.return_value.state = 'FAILED'

            # Simlulate stacktrace
            if idx == 1:
                mock_AsyncResult.return_value.traceback = 'STACKTRACE'
            else:
                mock_AsyncResult.return_value.traceback = None

            response = admin_client.get(
                '/celery-tracker/task-details/%s/' % task['id']
            )
            assert isinstance(response, HttpResponse)
            assert response.status_code == 200
