from django.forms import CharField, Form, TextInput, CheckboxInput, BooleanField
from django.core.validators import MinLengthValidator, EmailValidator

from authpage.validators import PhoneNumberValidator


class LoginForm(Form):
    username = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                "class": "input-field",
                "type": "username",
                "id": "username",
            }
        ),
        validators=[
            MinLengthValidator(10, "Имя пользователя слишком короткое"),
        ],
        required=True,
    )
    
    password = CharField(
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input-field",
                "type": "password",
                "id": "password",
            }
        ),
        required=True,
    )

    
    remember_me = BooleanField(
        widget=CheckboxInput(
            attrs={
                "type": "checkbox",
                "class": "remember-me",
                "id": "remember-me",
            },
        ),
        label="Запомнить меня на месяц",
        required=False,
    )


class SignupForm(Form):
    username = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                "class": "input-field",
                "type": "username",
                "id": "username",
            }
        ),
        validators=[
            MinLengthValidator(10, "Имя пользователя слишком короткое"),
        ],
        required=True,
    )
    
    phone_number = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Номер телефона",
                "class": "input-field",
                "type": "phone-number",
                "id": "phone-number",
            }
        ),
        validators=[
            PhoneNumberValidator(),
        ],
        required=True,
    )
    
    email = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Почта",
                "class": "input-field",
                "type": "email",
                "id": "email",
            }
        ),
        validators=[
            EmailValidator("Введите валидную почту"),
        ],
        required=True,
    )

    password = CharField(
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input-field",
                "type": "password",
                "id": "password",
            }
        ),
        required=True,
    )

    
    remember_me = BooleanField(
        widget=CheckboxInput(
            attrs={
                "type": "checkbox",
                "class": "remember-me",
                "id": "remember-me",
            },
        ),
        label="Запомнить меня на месяц",
        required=False,
    )
