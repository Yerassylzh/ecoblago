from django.contrib import admin
from django.urls import path, include

import ecoblago, authpage.urls, catalog.urls, profilepage.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(authpage.urls)),
    path("catalog/", include(catalog.urls)),
    path("profilepage/", include(profilepage.urls)),
]

if ecoblago.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
