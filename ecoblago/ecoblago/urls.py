from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.urls
from django.conf.urls.static import static
from django.conf import settings

import ecoblago, authpage.urls, catalog.urls, profilepage.urls, settingspage.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(authpage.urls)),
    path("", include(django.contrib.auth.urls)),
    path("catalog/", include(catalog.urls)),
    path("profilepage/", include(profilepage.urls)),
    path("settingspage/", include(settingspage.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if ecoblago.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
