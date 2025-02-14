import hashlib
from typing import Union
from datetime import datetime
from http import HTTPMethod

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.middleware.csrf import get_token
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext as _
from django.utils import translation
from django.utils.decorators import method_decorator

from login_required import LoginNotRequiredMixin

from authpage.forms import LoginForm, RegistrationForm
from authpage.models import User

class AuthpageView(LoginNotRequiredMixin, TemplateView):
    template_name = "authpage/authpage.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.LOGIN_OPTION = 0
        self.SIGNUP_OPTION = 1
        self.context = self.get_context_data(*args, **kwargs)
        self.context_ajax = self.get_context_ajax(*args, **kwargs)

        if translation.get_language() != self.context["lang"]:
            translation.activate(self.context["lang"])

    def get_context_ajax(self, *args, **kwargs):
        context = {}
        return context

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csrf_token"] = get_token(self.request)
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        context["next"] = self.request.GET.get("next", reverse("catalog:catalog"))
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.context["next"])

        elif "action" in self.request.GET:
            return self.handle_ajax()

        else:
            self.context["form"] = LoginForm()
            self.context["input_fields"] = self.get_auth_input_fields(self.LOGIN_OPTION)
            return self.render_to_response(self.context)

    def post(self, *args, **kwargs):
        if "action" in self.request.POST:
            return self.handle_ajax()
        else:
            return Http404("Cannot identify the purpose of POST request")

    def handle_ajax(self) -> JsonResponse:
        if self.request.method == HTTPMethod.POST:
            return self.handle_ajax_post()
    
        elif self.request.method == HTTPMethod.GET:
            return self.handle_ajax_get()

        else:
            return Http404(f"Unexpected ajax request. Request: {self.request}")

    def handle_ajax_get(self) -> JsonResponse:
        if self.request.GET.get("action") == "change-auth-type":
            auth_type = int(self.request.GET.get("auth_type"))
            self.context_ajax["input_fields"] = self.get_auth_input_fields(auth_type)
            return JsonResponse(data=self.context_ajax)
        else:
            raise Exception("Unexpected get request")

    def handle_ajax_post(self) -> JsonResponse:
        if self.request.POST.get("action") == "auth-user":
            return self.auth_user()

    def auth_user(self) -> JsonResponse:
        if int(self.request.POST.get("auth_type")) == self.LOGIN_OPTION:
            return self.login_user()

        elif int(self.request.POST.get("auth_type")) == self.SIGNUP_OPTION:
            return self.register_user()

        else:
            return Http404("Called 'auth_user' function but cannot identify the auth type")

    def login_user(self) -> JsonResponse:
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        user = authenticate(self.request, username=username, password=password)
        
        if not user:
            self.context_ajax.update({
                "success": False,
                "error_message": ("undef", _("Неверный логин или пароль"))
            })
            return JsonResponse(data=self.context_ajax)

        login(self.request, user)
        self.remember_user()

        self.context_ajax["success"] = True
        return JsonResponse(data=self.context_ajax)

    def register_user(self) -> JsonResponse:
        form = RegistrationForm(data=self.request.POST)
        if form.is_valid():
            form.save()
    
            self.remember_user()
            self.context_ajax["success"] = True
            return JsonResponse(data=self.context_ajax)
        else:
            form_errors = form.errors
            if len(form_errors) > 0:
                msg = list(form_errors.get_context()["errors"])[0]
                field = msg[0]
                error = msg[1][0]
                self.context_ajax["error_message"] = (field, error)
            self.context_ajax["success"] = False

            return JsonResponse(data=self.context_ajax)

    def change_auth_type(self) -> JsonResponse:
        auth_type = int(self.request.GET.get("auth_type"))
        self.context_ajax["input_fields"] = self.get_auth_input_fields(auth_type)
        return JsonResponse(data=self.context_ajax)

    def remember_user(self):
        days = None
        if self.request.POST.get("remember_me", "false") == "true":
            days = 1
        else:
            days = 30
        self.request.session.set_expiry(days * 24 * 60 * 60)

    def get_auth_input_fields(self, auth_type: int) -> list:
        if auth_type == self.LOGIN_OPTION:
            form: LoginForm = LoginForm()
            field_names = ["username", "password"]
        else:
            form: RegistrationForm = RegistrationForm()
            field_names = ["first_name", "last_name", "username", "phone_number", "email", "password1", "password2"]
    
        form_fields = []
        for field_name in field_names:
            form_fields.append((
                form[field_name].as_widget(),
                form[field_name].field.widget.attrs["placeholder"]
            ))

        return form_fields
