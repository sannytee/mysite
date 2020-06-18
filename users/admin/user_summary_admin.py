from django.contrib import admin
from django.db.models import Count, Case, When, IntegerField
from users.models import UserSummary


@admin.register(UserSummary)
class UserSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/users/user_summary_change_list.html'
    date_hierarchy = 'created_at'
    list_filter = ('country', 'gender', )
    actions = None

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_user_joined': Count('id'),
            'total_male_users': Count(Case(
                When(gender='1', then=1),
                output_field=IntegerField())),
            'total_female_users': Count(Case(
                When(gender='2', then=1),
                output_field=IntegerField())),
            'total_non_binary_users': Count(Case(
                When(gender='3', then=1),
                output_field=IntegerField()))
        }
        response.context_data['summary'] = list(
            qs
                .values('country')
                .annotate(**metrics)
                .order_by('total_user_joined')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response
