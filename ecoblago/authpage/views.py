import hashlib
from typing import Union
from http import HTTPMethod

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.middleware.csrf import get_token
from django.views import View

from authpage.forms import LoginForm, SignupForm
from authpage.models import User


class AuthpageView(View):
    authpage_template_url = "authpage/authpage.html"
    homepage_url_name = "catalog:catalog"

    LOGIN_OPTION = 0
    SIGNUP_OPTION = 1

    @staticmethod
    def get_password_hash(password: str) -> str:
        h = hashlib.new("SHA256")
        h.update(password.encode())
        return h.hexdigest()

    @staticmethod
    def set_any_error(form: Union[LoginForm, SignupForm], auth_errors: list, context: dict) -> str:
        if len(auth_errors) > 0:
            context["error_message"] = auth_errors[0]
            context["has_error_message"] = True

        elif len(form.errors) > 0:
            errors_data = form.errors.as_data()
            error_data = errors_data[
                list(
                    errors_data.keys()
                )[-1]
            ][-1]
            context["error_message"] = error_data.messages[0]
            context["has_error_message"] = True

        else:
            return None

    @staticmethod
    def save_user_login_info(request: HttpRequest, username: str, password: str, remember_me=False) -> None:
        if remember_me:
            request.session.update({
                "remembered": True,
            })
            request.session.set_expiry(30 * 24 * 60 * 60)  # for an entire month
        else:
            request.session.set_expiry(0)

        request.session.update({
            "username": username,
        })

    def login_user(self, request: HttpRequest, context) -> JsonResponse:
        auth_errors = []
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"].strip()
            password_hash = AuthpageView.get_password_hash(password)
            remember_me = form.cleaned_data["remember_me"]
            if len(User.objects.filter(username=username, password=password_hash)) > 0:
                context["success"] = True
                context["redirect_to"] = reverse(self.homepage_url_name)
                AuthpageView.save_user_login_info(request, username, password, remember_me)
                return JsonResponse(data=context)

            elif len(User.objects.filter(username=username)) > 0:
                auth_errors.append("Неверный пароль")

            else:
                auth_errors.append("Пользователь не найден")

        AuthpageView.set_any_error(form, auth_errors, context)
        return JsonResponse(data=context)

    def register_user(self, request: HttpRequest, context) -> JsonResponse:
        auth_errors = []
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"].strip()
            phone_number = form.cleaned_data["phone_number"].strip()
            email = form.cleaned_data["email"].strip()
            password_hash = AuthpageView.get_password_hash(password)
            remember_me = form.cleaned_data["remember_me"]

            if len(User.objects.filter(username=username)) > 0:
                auth_errors.append("Пользователь с таким именем уже существует.")

            else:
                User.objects.create(username=username, phone_number=phone_number, email=email, password=password_hash)
                context["success"] = True
                context["redirect_to"] = reverse(self.homepage_url_name)
    
            AuthpageView.save_user_login_info(request, username, password, remember_me)

        AuthpageView.set_any_error(form, auth_errors, context)
        return JsonResponse(data=context)

    def auth_user(self, request: HttpRequest, context) -> JsonResponse:
        if int(request.POST.get("auth_type")) == self.LOGIN_OPTION:
            return self.login_user(request, context)

        elif int(request.POST.get("auth_type")) == self.SIGNUP_OPTION:
            return self.register_user(request, context)

        else:
            return Http404("Called 'auth_user' function but cannot identify the auth type")

    def handle_ajax_get(self, request: HttpRequest, context: dict) -> JsonResponse:
        if request.GET.get("action") == "change-auth-type":
            auth_type = int(request.GET.get("auth_type"))
            context.update(self.get_auth_input_fields(auth_type))
            return JsonResponse(data=context)
        else:
            raise Exception("Unexpected get request")

    def handle_ajax_post(self, request: HttpRequest, context: dict) -> JsonResponse:
        if request.POST.get("action") == "auth-user":
            return self.auth_user(request, context)

    def handle_ajax(self, request: HttpRequest, context: dict) -> JsonResponse:
        if request.method == HTTPMethod.POST:
            return self.handle_ajax_post(request, context)
    
        elif request.method == HTTPMethod.GET:
            return self.handle_ajax_get(request, context)
        
        else:
            return Http404(f"Unexpected ajax request. Request: {request}")

    @staticmethod
    def get_auth_input_fields(auth_type: int) -> dict:
        data = {}
        if auth_type == AuthpageView.LOGIN_OPTION:
            form: LoginForm = LoginForm()
            form_fields = [
                form["username"].as_widget(),
                form["password"].as_widget(),
            ]
        else:
            form: SignupForm = SignupForm()
            form_fields = [
                form["username"].as_widget(),
                form["phone_number"].as_widget(),
                form["email"].as_widget(),
                form["password"].as_widget(),
            ]

        data = {
            "input_fields": form_fields,
        }
        return data

    @staticmethod
    def get_auth_form(auth_type: int) -> dict:
        data = AuthpageView.get_auth_input_fields(auth_type)
        data.update({
            "form": (LoginForm() if auth_type == AuthpageView.LOGIN_OPTION else SignupForm()),
        })

        return data
    
    def change_auth_type(self, request: HttpRequest) -> JsonResponse:
        auth_type = int(request.GET.get("auth_type"))
        if auth_type not in {self.LOGIN_OPTION, self.SIGNUP_OPTION}:
            raise Exception(f"Invalid auth type: {auth_type}")
        else:
            return JsonResponse(data=AuthpageView.get_auth_input_fields(auth_type))

    def get(self, request: HttpRequest):
        context = {
            "csrf_token": get_token(request),
        }

        if "remembered" in request.session:
            return redirect(reverse(self.homepage_url_name))

        elif "action" in request.GET:
            return self.handle_ajax(request, context)

        else:
            context.update(AuthpageView.get_auth_form(self.LOGIN_OPTION))
            return render(request, self.authpage_template_url, context)

    def post(self, request: HttpRequest):
        context = {
            "csrf_token": get_token(request),
        }

        if "action" in request.POST:
            return self.handle_ajax(request, context)
        else:
            return Http404("Cannot identify the purpose of POST request")
