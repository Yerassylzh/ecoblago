from django.forms import TextInput, CheckboxInput, BooleanField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext as _

from authpage.models import User


class RegistrationForm(UserCreationForm):
    remember_me = BooleanField(
        widget=CheckboxInput(
            attrs={
                "type": "checkbox",
                "class": "remember-me",
                "id": "remember-me",
            },
        ),
        label=_("Запомнить меня на месяц"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone_number"].widget = TextInput(
            attrs={
                "placeholder": _("Номер телефона"),
                "type": "text",
                "id": "phone-number",
            }
        )

        self.fields["email"].widget = TextInput(
            attrs={
                "placeholder": _("Почта"),
                "type": "text",
                "id": "email",
            }
        )

        self.fields["first_name"].widget = TextInput(
            attrs={
                "placeholder": _("Имя"),
                "type": "text",
                "id": "first_name",
            }
        )

        self.fields["last_name"].widget = TextInput(
            attrs={
                "placeholder": _("Фамилия"),
                "type": "text",
                "id": "last_name",
            }
        )

        self.fields["username"].widget = TextInput(
            attrs={
                "placeholder": _("Хэндл пользователя"),
                "type": "text",
                "id": "username",
            }
        )

        self.fields["password1"].widget = TextInput(
            attrs={
                "placeholder": _("Пароль"),
                "type": "password",
                "id": "password1",
            }
        )

        self.fields["password2"].widget = TextInput(
            attrs={
                "placeholder": _("Подтвердите пароль"),
                "type": "password",
                "id": "password2",
            }
        )

    def clean_phone_number(self):
        phone_number: str = "".join(
            list(
                filter(
                    lambda c: c not in "() -", self.cleaned_data.get(
                        "phone_number"
                    )
                )
            )
        )
        if phone_number.startswith("8"):
            phone_number = phone_number[1:]
        else:
            phone_number = phone_number[2:]  # it starts from +7

        return f"+7 ({phone_number[0:3]}) " + \
            f"{phone_number[3:6]}-{phone_number[6:]}"

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            "phone_number",
            'password1',
            'password2'
        ]


class LoginForm(AuthenticationForm):
    remember_me = BooleanField(
        widget=CheckboxInput(
            attrs={
                "type": "checkbox",
                "class": "remember-me",
                "id": "remember-me",
            },
        ),
        label=_("Запомнить меня на месяц"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = TextInput(
            attrs={
                "placeholder": _("Имя пользователя"),
                "type": "text",
                "id": "username",
            }
        )

        self.fields["password"].widget = TextInput(
            attrs={
                "placeholder": _("Пароль"),
                "type": "password",
                "id": "password",
            }
        )

    class Meta:
        model = User
        fields = ['username', 'password']
