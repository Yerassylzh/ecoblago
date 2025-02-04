import os
from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.middleware.csrf import get_token
from django.contrib.auth.models import AbstractUser 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import ImageField

from authpage.models import User
from django.contrib.auth import logout

class SettingspageView(TemplateView):
    template_name = "settingspage/settingspage.html"

    def get(self, *args) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def post(self, *args) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()
        return Http404()
    
    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST["action"]
        if "change-password" == action:
            return self.change_password()
        elif "logout" == action:
            return self.logout_user()
        elif "delete-account" == action:
            return self.delete_user()
        elif "change-theme" == action:
            return self.change_theme()
        return Http404()
    
    def change_theme(self) -> JsonResponse:
        theme = self.request.POST["theme"]
        response = JsonResponse({"success": True})
        response.set_cookie("theme", theme, max_age=60*60*24*365)
        return response

    def logout_user(self) -> JsonResponse:
        logout(self.request)
        self.request.session.delete()
        return JsonResponse({"success": True})
    
    def delete_user(self) -> JsonResponse:
        user = self.request.user
        user.delete()
        logout(self.request)
        self.request.session.delete()
        return JsonResponse({"success": True})

    def change_password(self) -> JsonResponse:
        new_password = self.request.POST["new_password"]
        try:
            validate_password(new_password)
        except ValidationError as e:
            return JsonResponse({"success": False, "error_message": e.messages[0]})

        user = self.request.user
        user.set_password(new_password)
        user.save()

        return JsonResponse({"success": True})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csrf_token"] = get_token(self.request)
        context["user_logined"] = ("remembered" in self.request.session)
        context["theme"] = (self.request.COOKIES["theme"] if "theme" in self.request.COOKIES else "light")

        return context

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)

        self.context = self.get_context_data()
        self.user = None
        if self.context["user_logined"] == True:
            self.user = get_object_or_404(User, username=self.request.session["username"])

        self.context["my_user"] = self.user
