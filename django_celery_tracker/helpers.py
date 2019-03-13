def get_task_created_item(t):
    return {
        'id': t.task_id,
        'content': '(created) ' + t.task_name,
        'type': 'point',
        'start': t.created.isoformat(),
        'className': 'created',
    }


def get_task_data(t):
    if t.post_state == 'SUCCESS':
        className = 'success'
    elif t.post_state == 'PREMATURE_SHUTDOWN':
        className = 'premature'
    elif t.post_state == 'FAILURE':
        className = 'failed'
    else:
        className = 'inprogress'

    data = {
        'id': t.task_id,
        'content': "%s (%s)" % (t.task_name, className,),
        'start': t.started.isoformat(),
        'progress': t.progress,
        'progress_target': t.progress_target,
        'post_state': t.post_state,
        'className': className,
    }

    if t.completed is not None:
        data['end'] = t.completed.isoformat()
    else:
        data['content'] = '(running) ' + t.task_name

    return data
