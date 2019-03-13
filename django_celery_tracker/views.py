import json
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import HttpResponse, SimpleTemplateResponse
from django.utils.dateparse import parse_datetime
from celery.result import AsyncResult

from django_celery_tracker.decorators import admin_required
from django_celery_tracker.helpers import (
    get_task_created_item,
    get_task_data,
)
from django_celery_tracker.models import CeleryTask


@admin_required
def tracker_dashboard(request):
    context = {
        "title": "Celery Dashboard",
        "has_permission": True,
        "user": request.user,
    }

    return SimpleTemplateResponse(
        "celery_tracker/timeline_dashboard.html",
        context=context,
    )


@admin_required
def timeline_page_data(request):
    if 'date' not in request.GET:
        return HttpResponse(
            json.dumps({'error': 'Must specify date'}),
            content_type='application/json',
            status=400,
        )
    start_time = parse_datetime(request.GET['date'])
    end_time = start_time + timedelta(days=1)

    created = CeleryTask.objects.filter(
        Q(started__isnull=True),
        Q(created__gte=start_time, created__lt=end_time)
    )
    page = [get_task_created_item(t) for t in created]

    tasks = CeleryTask.objects.filter(
        Q(started__isnull=False),
        Q(
            completed__isnull=True,
            started__gte=start_time,
            started__lt=end_time
        ) | (
            Q(completed__isnull=False) & (
                Q(
                    started__gte=start_time,
                    started__lt=end_time,
                ) | Q(
                    started__lt=start_time,
                    completed__gte=start_time,
                )
            )
        ),
    )
    page = page + [get_task_data(t) for t in tasks]

    return HttpResponse(
        json.dumps(page),
        content_type='application/json',
    )


@admin_required
def task_details(request, task_id):
    task = get_object_or_404(CeleryTask, task_id=task_id)
    res = AsyncResult(task_id)

    details = {
        'task_name': task.task_name,
        'task_id': task_id,
        'args': task.args,
        'created': task.created,
        'started': task.started,
        'completed': task.completed,
    }

    try:
        details['state'] = res.state
        if res.traceback is not None:
            details['traceback'] = str(res.traceback).replace('\n', '<br/>')
    except TypeError:
        # Celery doesn't have a record of this uuid
        details['state'] = 'UNKNOWN'

    if task.post_state:
        details['state'] = task.post_state

    return HttpResponse(
        json.dumps(details, cls=DjangoJSONEncoder),
        content_type='application/json',
    )
