Date.prototype.toDateInputValue = (function() {
  var local = new Date(this);
  local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
  return local.toJSON().slice(0,10);
});
Date.prototype.addDays = function(days) {
  var date = new Date(this.valueOf());
  date.setDate(date.getDate() + days);
  return date;
}
Number.prototype.pad = function(size) {
  var s = String(this);
  while (s.length < (size || 2)) {s = "0" + s;}
  return s;
}

let timeline = null;
let selectedItem = null;

function getTaskDetails() {
  if (!selectedItem) {
    return;
  }

  $('#left-pane').addClass('center');
  $('#placeholder').html('Loading...');
  $('#placeholder').show();
  $('#task-details').hide();

  
  setTimeout(function() {
    $.get(
      'task-details/'+selectedItem+'/',
      function(task) {
        let created = new Date(task.created);
        let started = new Date(task.started);
        let completed = new Date(task.completed);

        $('#task-details #task_name').html(task.task_name);
        $('#task-details #uuid').html(task.task_id);

        if (task.args) {
          $('#args').html(task.args);
          $('#args-container').show();
        } else {
          $('#args-container').hide();
        }

        $('#task-details #state').html(task.state);
        let waited;
        if (task.started) {
          waited = vis.moment.duration(vis.moment(started).diff(vis.moment(created)));
        } else {
          waited = vis.moment.duration(vis.moment().diff(vis.moment(created)));
        }
        $('#task-details #started').html(
            (task.started ? started.toLocaleTimeString() : ' -- ') +
            ' (in queue '+waited.humanize()+')'
        );
        
        if (task.completed) {
          let elapsed = vis.moment.duration(vis.moment(completed).diff(vis.moment(started)));
          $('#task-details #completed').html(
            completed.toLocaleTimeString() + ' (took ' + elapsed.humanize() + ')'
          );
        } else {
          $('#task-details #completed').html(' -- ');
        }

        if (task.traceback) {
          $('#traceback').html(task.traceback);
          $('#traceback-container').show();
        } else {
          $('#traceback-container').hide();
        }

        $('#left-pane').removeClass('center');
        $('#placeholder').hide();
        $('#task-details').show();
      }
    ).fail(function() {
      $('#placeholder').html('Failed to load details');
    });
  }, 500);
}

function clearTaskDetails() {
  $('#task-details').hide();
  $('#left-pane').addClass('center');
  $('#placeholder').html('Select a task for more details');
  $('#placeholder').show();
}

function getDay(clear = true) {
  let val = $('#date-picker').val();

  if (clear && timeline) {
    timeline.off('select');
    timeline.destroy();
    timeline = null;
    clearTaskDetails();
  }

  if (!val) {
    return;
  }

  $('#date-picker').attr('disabled', 'disabled');
  $('#refresh-wrapper').html('<i class="spinner"></i>');

  // Create date object from date picker
  let date = new Date(val);

  let offset = date.getTimezoneOffset();
  let mins = Math.abs(offset % 60);
  let hrs = Math.trunc(offset / 60);
  offset = (hrs < 0 ? '+' : '-') + Math.abs(hrs).pad() + ':'+mins.pad();
  dateStr = val + 'T00:00:00' + offset;

  let start = date;
  let end = start.addDays(1);

  start = vis.moment(start).add(-vis.moment(date).utcOffset(), 'minutes').valueOf();
  end = vis.moment(end).add(-vis.moment(date).utcOffset(), 'minutes').valueOf();

  setTimeout(function() {
    $.get(
      'timeline-data/?date='+encodeURIComponent(dateStr),
      function(items) {
        if (clear) {
          var options = {
            start: start,
            end: end,
            min: start,
            max: end,
            format: {
              minorLabels: {
                millisecond: 'SSS',
                second: 's',
                minute: 'h:mma',
                hour: 'ha',
              },
              majorLabels: {
                millisecond: 'hh:mm:ss a',
                second: 'D MMMM hh:mm a',
                minute: 'ddd D MMMM',
              }
            }
          };

          var container = document.getElementById('my-timeline');
          timeline = new vis.Timeline(container, items, options);
          timeline.on('select', function(props) {
            if (props.items.length > 0) {
              selectedItem = props.items[0];
              getTaskDetails();
            } else {
              selectedItem = null;
              clearTaskDetails();
            }
          });
        } else {
          timeline.setItems(items);
          if (selectedItem) {
            timeline.setSelection(selectedItem);
          }
        }

        $('#date-picker').removeAttr('disabled');
        $('#refresh-wrapper').html('<a href="javascript:getDay(false); getTaskDetails()" class="refresh"></a>');
      }
    );
  }, 500);
}
