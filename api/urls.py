from django.urls import path
from . import views

urlpatterns = [
    # authentication api urls
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('reset-password/', views.PasswordUpdateView.as_view(), name='reset-password'),
    # member update and delete api url
    path('member/', views.MemberView.as_view(), name='member'),
    # invite member and accept invite api urls
    path('invite-member/', views.InviteMemberView.as_view(), name='invite-member'),
    path('accept-invite/<uuid:token>/', views.AcceptInviteView.as_view(), name='accept-invite'),
    # stats api urls
    path('role/users/', views.user_roles_count, name='role-users-count'),
    path('organization/users/', views.organization_users_count, name='organization-users-count'),
    path('organization-role/users/', views.organization_role_users_count, name='organization-role-users-count'),
]
