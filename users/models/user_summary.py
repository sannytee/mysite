from users.models import User


class UserSummary(User):
    class Meta:
        proxy = True
        verbose_name = 'User Summary'
        verbose_name_plural = 'Users Summary'