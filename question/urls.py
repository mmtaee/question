from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from .routers import router
from .swagger import swagger


urlpatterns = [
    path("api/", include(router.urls)),
    path("help/", swagger),
]

if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]
