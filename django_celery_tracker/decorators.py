from django.shortcuts import redirect
from django.urls import reverse


# Similar to user_passes_test but redirects to django admin login
def admin_required(func):
    def as_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(
                '%s?next=%s' % (reverse('admin:login'), request.path)
            )

        return func(request, *args, **kwargs)
    return as_view
