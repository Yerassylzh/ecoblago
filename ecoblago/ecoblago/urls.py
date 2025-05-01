from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.urls
from django.conf.urls.static import static
from django.urls import include, re_path
from django.conf import settings
from django.views.i18n import JavaScriptCatalog

import ecoblago, authpage.urls, catalog.urls, profilepage.urls, settingspage.urls, rosetta.urls, policy.urls
from serve_media.views import serve_media

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(authpage.urls)),
    path("", include(django.contrib.auth.urls)),
    path("catalog/", include(catalog.urls)),
    path("profilepage/", include(profilepage.urls)),
    path("settingspage/", include(settingspage.urls)),
    path("policy/", include(policy.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
]

if not settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>/', serve_media, name='serve_media'),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include(rosetta.urls))
    ]