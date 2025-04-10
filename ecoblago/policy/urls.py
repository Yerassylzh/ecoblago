from django.urls import path

from policy import views

app_name = "policy"

urlpatterns = [
    path("terms-of-usage", views.view, name="terms-of-usage"),
]
