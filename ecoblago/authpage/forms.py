from django.forms import CharField, TextInput, CheckboxInput, BooleanField
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from authpage.models import User
from authpage.validators import PhoneNumberValidator

class RegistrationForm(UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone_number"].widget = TextInput(
            attrs={
                "placeholder": "Номер телефона",
                "type": "text",
                "id": "phone-number",
            }
        )

        self.fields["email"].widget = TextInput(
            attrs={
                "placeholder": "Почта",
                "type": "text",
                "id": "email",
            }
        )

        self.fields["first_name"].widget = TextInput(
            attrs={
                "placeholder": "Имя",
                "type": "text",
                "id": "first_name",
            }
        )

        self.fields["last_name"].widget = TextInput(
            attrs={
                "placeholder": "Фамилия",
                "type": "text",
                "id": "last_name",
            }
        )

        self.fields["username"].widget = TextInput(
            attrs={
                "placeholder": "Хэндл пользователя",
                "type": "text",
                "id": "username",
            }
        )

        self.fields["password1"].widget = TextInput(
            attrs={
                "placeholder": "Пароль",
                "type": "password",
                "id": "password1",
            }
        )

        self.fields["password2"].widget = TextInput(
            attrs={
                "placeholder": "Подтвердите пароль",
                "type": "password",
                "id": "password2",
            }
        )

    def clean_phone_number(self):
        phone_number : str = "".join(list(filter(lambda c: c not in "() -", self.cleaned_data.get("phone_number"))))
        if phone_number.startswith("8"):
            phone_number = phone_number[1:]
        else:
            phone_number = phone_number[2:]  # it starts from +7

        cleaned_phone_number = f"+7 ({phone_number[0:3]}) {phone_number[3:6]}-{phone_number[6:]}"
        return cleaned_phone_number

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', "phone_number", 'password1', 'password2']


class LoginForm(AuthenticationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                "type": "text",
                "id": "username",
            }
        )

        self.fields["password"].widget = TextInput(
            attrs={
                "placeholder": "Пароль",
                "type": "password",
                "id": "password",
            }
        )

    class Meta:
        model = User
        fields = ['username', 'password']
