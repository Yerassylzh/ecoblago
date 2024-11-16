import hashlib

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from loginpage.forms import LoginForm, SignupForm
from loginpage.models import User

current_auth_option = 0
USER_PHONE = None


def get_filtered_phone_number(phone_number: str) -> str:
    return "".join(
        list(
            filter(
                lambda c: "0" <= c <= "9",
                phone_number,
            ),
        ),
    )


def get_password_hash(password: str) -> str:
    h = hashlib.new("SHA256")
    h.update(password.encode())
    return h.hexdigest()


def login(request: HttpRequest) -> HttpResponse:
    global current_auth_option

    context = {
        "main_text": "ВХОД",
        "button_text": "Продолжить",
        "auth_option": current_auth_option,
    }
    
    form = LoginForm()
    auth_errors = []
    if request.method.upper() == "POST":
        if "auth-option-signup" in request.POST:
            context["auth_option"] = 1
            form = SignupForm()

        elif "auth-option-login" in request.POST:
            context["auth_option"] = 0
            form = LoginForm()
        
        elif "commit-button" in request.POST:
            if current_auth_option == 0:
                form = LoginForm(request.POST)
                if form.is_valid():
                    phone = get_filtered_phone_number(form.cleaned_data["phone"])
                    password = get_password_hash(form.cleaned_data["password"])
                    if len(User.objects.filter(phone=phone, password=password)) > 0:
                        return redirect("Here should be catalog, but i seems i didn't implemented it yet =(")
                    auth_errors.append("Пользователь не найден")

            else:
                form = SignupForm(request.POST)

                if form.is_valid():
                    first_name = form.cleaned_data["first_name"]
                    last_name = form.cleaned_data["last_name"]
                    phone = get_filtered_phone_number(form.cleaned_data["phone"])
                    email = form.cleaned_data["email"]
                    password = get_password_hash(form.cleaned_data["password"])

                    if len(User.objects.filter(phone=phone)) > 0:
                        auth_errors.append("Пользователь с таким номером телефона уже существует.")
                    elif len(User.objects.filter(email=email)) > 0:
                        auth_errors.append("Пользователь с такой почтой уже существует.")
                    else:
                        User.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
                        return redirect("Here should be catalog, but i seems i didn't implemented it yet =(")

    context["form"] = form
    if len(form.errors) > 0:
        errors_data = form.errors.as_data()
        error_data = errors_data[
            list(
                errors_data.keys()
            )[0] # Рандомный ключ
        ][0]  # берет лишь одну ошибку для красивого отображения
        context["error_message"] = error_data.message

    elif len(auth_errors) > 0:
        context["error_message"] = auth_errors[0]

    current_auth_option = context["auth_option"]
    return render(request, "loginpage/loginpage.html", context=context)
