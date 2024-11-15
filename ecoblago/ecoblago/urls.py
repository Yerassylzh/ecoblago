from django.contrib import admin
from django.urls import path, include

import ecoblago, loginpage.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(loginpage.urls)),
]

if ecoblago.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
