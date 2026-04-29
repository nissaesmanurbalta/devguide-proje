from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('education/', include('education.urls')),
    path('mentoring/', include('mentoring.urls')),
]
