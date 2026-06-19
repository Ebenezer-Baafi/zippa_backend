from django.contrib import admin
from django.urls    import path, include
from django.conf    import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/riders/', include('riders.urls')),
    path('api/v1/jobs/', include('jobs.urls')),
    path('api/v1/negotiations/', include('negotiations.urls')),
    path('api/v1/ratings/', include('ratings.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/cores/', include('cores.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )