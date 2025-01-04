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

from authpage.forms import LoginForm, RegistrationForm
from authpage.models import User


class AuthpageView(TemplateView):
    template_name = "authpage/authpage.html"

    def get(self, *args, **kwargs):
        if "remembered" in self.request.session:
            return redirect(reverse(self.catalog_url))

        elif "action" in self.request.GET:
            return self.handle_ajax()

        else:
            self.context.update({
                "form": LoginForm(),
            })
            self.context.update(
                self.get_auth_input_fields(self.LOGIN_OPTION),
            )
            return render(self.request, self.template_name, self.context)

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
            self.context_ajax.update(self.get_auth_input_fields(auth_type))
            return JsonResponse(data=self.context_ajax)
        else:
            raise Exception("Unexpected get request")

    def handle_ajax_post(self) -> JsonResponse:
        if self.request.POST.get("action") == "auth-user":
            return self.auth_user()
        else:
            raise Exception(f"Cannot identify the purpose of ajax request: {self.request}")

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
                "error_message": ("undef", "Пользователь не найден")
            })
            return JsonResponse(data=self.context_ajax)

        login(self.request, user)
        self.remember_user()
        self.context_ajax.update({
            "success": True,
            "redirect_to": reverse(self.catalog_url),
        })
        return JsonResponse(data=self.context_ajax)
        
    def register_user(self) -> JsonResponse:
        form = RegistrationForm(data=self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.phone_number = form.cleaned_data["phone_number"]
            user.save()

            login(self.request, user)
            self.remember_user()
            self.context_ajax.update({
                "success": True,
                "redirect_to": reverse(self.catalog_url),
            })
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
        if auth_type not in {self.LOGIN_OPTION, self.SIGNUP_OPTION}:
            raise Exception(f"Invalid auth type: {auth_type}")
        else:
            return JsonResponse(data=self.get_auth_input_fields(auth_type))

    def remember_user(self):
        remember_me = self.request.POST.get("remember_me")
        self.request.session["remembered"] = True
        self.request.session["username"] = self.request.POST.get("username")
        if remember_me == "true":
            self.request.session.set_expiry(30 * 24 * 60 * 60)
        else:
            self.request.session.set_expiry(12 * 60 * 60)

    def get_auth_input_fields(self, auth_type: int) -> dict[str, list]:
        if auth_type == self.LOGIN_OPTION:
            form: LoginForm = LoginForm()
            form_fields = [
                form["username"].as_widget(),
                form["password"].as_widget(),
            ]
        else:
            form: RegistrationForm = RegistrationForm()
            form_fields = [
                form["first_name"].as_widget(),
                form["last_name"].as_widget(),
                form["username"].as_widget(),
                form["phone_number"].as_widget(),
                form["email"].as_widget(),
                form["password1"].as_widget(),
                form["password2"].as_widget(),
            ]

        return {
            "input_fields": form_fields,
        }

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.catalog_url = "catalog:catalog"
        self.LOGIN_OPTION = 0
        self.SIGNUP_OPTION = 1
        self.context = self.get_context_data()
        self.context_ajax = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csrf_token"] = get_token(self.request)
        return context
