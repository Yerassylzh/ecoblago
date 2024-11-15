from django.urls import path, include

import loginpage.views

app_name = "loginpage"

urlpatterns = [
    path("", loginpage.views.login, name="login"),
]
