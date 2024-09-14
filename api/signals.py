from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sites.models import Site
from .models import Invitation
#
# User = get_user_model()
#
#
# @receiver(user_logged_in)
# def send_login_alert(sender, request, user, **kwargs):
#     """
#     Function to send login alert mail once the user logs in to the system.
#     :param sender:
#     :param request:
#     :param user:
#     :param kwargs:
#     :return:
#     """
#     subject = 'Login Alert: Account logged in!!'
#     message = f'Dear {user.email},\n\nYou just logged in to your account via our system.\nPlease enjoy your session!'
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )
#
#
# @receiver(post_save, sender=User)
# def send_password_update_email(sender, instance, created, **kwargs):
#     """
#     Function to send password updated alert mail once the user changes his password
#     :param sender:
#     :param instance:
#     :param created:
#     :param kwargs:
#     :return:
#     """
#     if not created:
#         if getattr(instance, 'password_changed', False):
#             subject = 'Login Alert: Account logged in!!'
#             message = f'Dear {instance.email},\n\nYour new password has been successfully updated.'
#             send_mail(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [instance.email],
#                 fail_silently=False,
#             )
#
#
# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     """
#     Function to send invite mail along with login url once the user registers successfully into the system.
#     :param sender:
#     :param instance:
#     :param created:
#     :param kwargs:
#     :return:
#     """
#     if created:
#         site = Site.objects.get_current()
#         domain = site.domain
#         protocol = 'https' if settings.USE_HTTPS else 'http'
#         login_url = f"{protocol}://{domain}{reverse('sign-in')}"
#         subject = 'New User Created: User account creation successful!!'
#         message = f'Dear {instance.email},\n\nThank you for registering in our system.\n Login using the below link' \
#                   f' {login_url}.'
#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
#         )

