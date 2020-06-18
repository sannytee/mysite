from django.contrib.auth.admin import UserAdmin as BaseAdminUser
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import path

from users.forms import UserCreationForm, UserChangeForm, MailForm
from users.models import User


class UserAdmin(BaseAdminUser):
    """Customize superadmin users view."""
    add_form = UserCreationForm
    form = UserChangeForm

    change_list_template = "admin/users/change_list.html"
    actions = ['change_user_status']

    search_fields = ('email', 'username')
    list_display = ('username', 'email', 'first_name', 'last_name', 'active', 'staff')
    list_filter = ('staff', 'admin', 'active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Personal info', {'fields': ('birthday', 'gender', 'country')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'password1', 'password2', 'birthday', 'gender', 'country',
                       'admin', 'staff', 'active'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('send-email/', self.send_mail),
        ]
        return my_urls + urls

    def change_user_status(self, request, queryset):
        for user in queryset:
            user.active = not user.active
            user.save()

    change_user_status.short_description = 'Change selected user status'

    def send_mail(self, request):
        form = MailForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            subject = form.cleaned_data.get("subject")
            content = form.cleaned_data.get("content")
            user_email_instance = self.model.objects.values_list('email') \
                .filter(staff=False, active=True) \
                .exclude(email='')
            users_email = list(map(lambda x: x[0], user_email_instance))
            if len(users_email) > 0:
                send_mail(subject, content, 'noreply@adminsite.com', users_email)
                messages.success(request, 'Mail successfully sent to users')
                return HttpResponseRedirect('/admin/users/user/')
            else:
                messages.error(request, 'Confirm existing users are active with valid mails')

        context = {
            "form": form
        }
        return render(request, "admin/users/email_form.html", context)


admin.site.register(User, UserAdmin)
