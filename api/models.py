from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator


class Organisation(models.Model):
    name = models.CharField(max_length=50, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default={}, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


# class User(models.Model):
#     email = models.EmailField(unique=True, null=False)
#     password = models.CharField(max_length=50, unique=False, null=False)
#     profile = models.JSONField(default={}, null=False)
#     status = models.IntegerField(default=0, null=False)
#     settings = models.JSONField(default={}, null=True)
#     created_at = models.DateTimeField(null=True)
#     updated_at = models.DateTimeField(null=True)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator()])  # Use email for authentication
    profile = models.JSONField(default={}, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default={}, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    objects = UserManager()  # Link the manager

    USERNAME_FIELD = 'email'  # Set the field used for authentication

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='roles', null=False)


class Member(models.Model):
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='members', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='members', null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default={}, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
