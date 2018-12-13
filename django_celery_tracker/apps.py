"""Application configuration."""
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

__all__ = ['CeleryTrackerConfig']


class CeleryTrackerConfig(AppConfig):
    """Default configuration for the django_celery_tracker app."""

    name = 'django_celery_tracker'
    label = 'django_celery_tracker'
    verbose_name = _('Celery Tracker')

    def ready(self):
        from django_celery_tracker import signals  # noqa F401
