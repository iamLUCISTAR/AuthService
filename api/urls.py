from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # authentication api urls
    path('auth/', include('api.auth.urls')),

    # stats api urls
    path('stats/', include('api.stats.urls')),

    # update, delete and invite member and accept invite api urls
    path('member/', views.MemberView.as_view(), name='member'),
    path('invite-member/', views.InviteMemberView.as_view(), name='invite-member'),
    path('accept-invite/<uuid:token>/', views.AcceptInviteView.as_view(), name='accept-invite'),

    # jwt token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
