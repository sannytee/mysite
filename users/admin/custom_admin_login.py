from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect


class CustomAdminLogin(LoginView):
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(settings.ADMIN_LOGIN_REDIRECT_URL)
