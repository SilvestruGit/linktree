from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user."""
        if email is None or len(email) <= 7:
            raise(ValueError("The email is not valid."))
        user = self.model(email=self._normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def _normalize_email(self, email):
        """Returns normalized emails."""
        email = email.split('@')
        email = email[0] + '@' + email[1].lower()
        return email


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email