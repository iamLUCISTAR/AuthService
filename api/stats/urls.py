from django.urls import path
from . import views

urlpatterns = [
    path('role-users/', views.user_roles_count, name='role-users-count'),
    path('organization-users/', views.organization_users_count, name='organization-users-count'),
    path('organization-role-users/', views.organization_role_users_count, name='organization-role-users-count'),
]
