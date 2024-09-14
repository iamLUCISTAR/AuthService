import datetime
import uuid

from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.conf import settings


class Organization(models.Model):
    """
    Model for storing organization details
    """
    name = models.CharField(max_length=50, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


class CustomUserManager(BaseUserManager):
    """
    Manager class for handling the user model
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    Model for storing user details
    """
    def __init__(self, *args, **kwargs):
        self.password_changed = False
        super().__init__(*args, **kwargs)

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    profile = models.JSONField(default=dict, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if self.pk:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.password != self.password:
                self.password_changed = True
        else:
            self.password_changed = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Role(models.Model):
    """
    Model for storing role details of an organization.
    """
    name = models.CharField(max_length=50, default='owner', null=False)
    description = models.TextField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='roles', null=False)


class Member(models.Model):
    """
    Model for storing member details along with user, role and organization details.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members', null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='members', null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='members', null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'organization'], name='unique_user_organization')
        ]


def get_default_expiration():
    """
    Function to return expiration time for invitation token
    :return:
    """
    return timezone.now() + datetime.timedelta(hours=24)


class Invitation(models.Model):
    """
    Model for storing invitation details
    """
    email = models.EmailField(validators=[EmailValidator()])
    invited_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users', null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role', null=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField(default=get_default_expiration)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)

    def accept(self):
        self.is_accepted = True
        self.accepted_at = datetime.datetime.now()
        self.save()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def send_invite_mail(self):
        site = Site.objects.get_current()
        domain = site.domain
        invite_url = f"https://{domain}{reverse('accept-invite', args=[self.token])}"
        subject = 'Member Invitation: We are happy to invite you!!'
        message = f'Dear {self.email},\n\nClick on the link to accept the invitation from ' \
                  f'{self.invited_by.email} for joining as a member of our organization.\n' \
                  f'{invite_url}'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
