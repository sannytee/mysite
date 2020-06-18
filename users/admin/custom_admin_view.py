from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext as _
from django.conf import settings
from users.admin.custom_admin_login import CustomAdminLogin


class CustomAdminSite(AdminSite):
    @never_cache
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            return HttpResponseRedirect(settings.ADMIN_LOGIN_REDIRECT_URL)

        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            'REDIRECT_FIELD_NAME': settings.ADMIN_LOGIN_REDIRECT_URL,
        }
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        return CustomAdminLogin.as_view(**defaults)(request)


site = CustomAdminSite()
