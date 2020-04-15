from celery.signals import before_task_publish, task_prerun, task_postrun


@before_task_publish.connect
def task_publish_handler(sender=None, headers=None, body=None, **kwargs):
    from django_celery_tracker.models import CeleryTask
    info = headers if 'task' in headers else body

    CeleryTask.objects.get_or_create(
        task_id=info['id'], task_name=info['task'], args=info['argsrepr']
    )


@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, **kwargs):
    from django_celery_tracker.models import CeleryTask
    from django.utils import timezone

    t = CeleryTask.objects.get_or_create(task_id=task_id)[0]
    t.started = timezone.now()
    t.save(update_fields=['started'])


@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, state=None, **kwargs):
    from django_celery_tracker.models import CeleryTask
    from django.utils import timezone

    t = CeleryTask.objects.get_or_create(task_id=task_id)[0]
    t.completed = timezone.now()
    if state is not None:
        t.post_state = state
    else:
        t.post_state = 'PREMATURE_SHUTDOWN'
    t.save(update_fields=['completed', 'post_state'])
