# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0]

### Added
- Now supports django `4.x`

## [1.2.0]

### Added
- Now supports celery `5.x`

## [1.1.1]

### Added
- Now passing `update_fields` to calls to `CeleryTask.save()` for those connecting to the `post_save` signal

## [1.1.0]

### Added
- Dashboard view included in `django_celery_tracker.urls`
- Field `args` to `CeleryTask` model (don't forget to run `./manage.py migrate`)

## [1.0.1]

### Fixed
- `README.md` now properly updated to `django_celery_tracker`

### Added
- Disclaimer for database usage

[Unreleased]: https://github.com/chris-allen/django-celery-tracker/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/chris-allen/django-celery-tracker/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/chris-allen/django-celery-tracker/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/chris-allen/django-celery-tracker/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/chris-allen/django-celery-tracker/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/chris-allen/django-celery-tracker/compare/v1.0.0...v1.0.1
