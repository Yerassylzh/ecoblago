from django.urls import path

from profilepage import views

app_name = "profilepage"

urlpatterns = [
    path("<int:pk>/", views.ProfilepageView.as_view(), name="profilepage"),
]
