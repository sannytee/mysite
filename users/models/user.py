from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.models import UsersManager

GENDER_CHOICES =(
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Not specified"),
)


class User(AbstractBaseUser, PermissionsMixin):
    """Users model."""

    username = models.CharField(unique=True, max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=30, null=False)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=False)
    # password = models.CharField(max_length=128, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=3,
        choices=GENDER_CHOICES
    )
    country = models.CharField(max_length=50, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = UsersManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    class Meta:
        """Define metadata options."""

        ordering = ('pk',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """Return object's string representation."""
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active(self):
        """Check if user is active."""
        return self.active

    @property
    def is_staff(self):
        """Check whether user is staff."""
        return self.staff

    @property
    def is_superuser(self):
        """Check whether user is super admin."""
        return self.admin

    def save(self, *args, **kwargs):
        self.country = self.country.lower()
        return super(User, self).save(*args, **kwargs)