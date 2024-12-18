from django.contrib import admin
from django.urls import path, include

import ecoblago, authpage.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(authpage.urls)),
]

if ecoblago.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
