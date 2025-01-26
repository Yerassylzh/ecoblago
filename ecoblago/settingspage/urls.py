from django.urls import path, include

from settingspage.views import SettingspageView

app_name = "settingspage"

urlpatterns = [
    path("", SettingspageView.as_view(), name="settingspage"),
]
