"""
URL configuration for hostel_ai project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "બોટ મેનૂ AI સહાયક Admin Panel"
admin.site.site_title = "Boat Menu Admin"
admin.site.index_title = "Welcome to Boat Menu Management System"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assistant.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
