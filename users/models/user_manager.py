from django.contrib.auth.models import BaseUserManager


class UsersManager(BaseUserManager):
    """Users model manager."""

    def create_user(
            self,
            username,
            email,
            password=None,
            is_active=True,
            is_staff=False,
            is_admin=False):
        """Create a user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email):
        """Create a regular user."""
        return self.create_user(email)

    def create_superuser(self, username, email, password):
        """Create a superuser."""
        return self.create_user(
            username,
            email,
            is_admin=True,
            is_active=True,
            is_staff=True,
            password=password)