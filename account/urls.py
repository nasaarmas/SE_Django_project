from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete-notification/<int:notification_id>/', DeleteNotificationView.as_view(), name='delete-notification'),
    path('accept-invitation/<int:social_group_id>/<int:notification_id>/', AcceptInvitationView.as_view(),
         name='accept-invitation'),
]
