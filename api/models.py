from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator


class Organization(models.Model):
    name = models.CharField(max_length=50, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    def __init__(self, *args, **kwargs):
        self.password_changed = False
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.password != self.password:
                self.password_changed = True
        else:
            self.password_changed = False
        super().save(*args, **kwargs)

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    profile = models.JSONField(default=dict, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    # def __str__(self):
    #     return self.email


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='roles', null=False)


class Member(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members', null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users', null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='members', null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'organization'], name='unique_user_organization')
        ]
