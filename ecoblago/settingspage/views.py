import os
from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import AbstractUser 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db.models import ImageField

from authpage.models import User

class SettingspageView(TemplateView):
    template_name = "settingspage/settingspage.html"

    def get(self, request) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csrf_token"] = get_token(self.request)
        context["user_logined"] = ("remembered" in self.request.session)

        return context

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)

        self.context = self.get_context_data()
        self.user = None
        if self.context["user_logined"] == True:
            self.user = get_object_or_404(User, username=self.request.session["username"])

        self.context["my_user"] = self.user
