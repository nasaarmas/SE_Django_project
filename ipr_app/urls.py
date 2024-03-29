from django.contrib import admin
from django.urls import path, include

from account.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('social_group.urls')),
    path('', include('event.urls')),
    # ... other patterns ...
]
