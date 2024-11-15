from django.forms import CharField, Form, TextInput, EmailInput

from loginpage.validators import validate_phone_number


class LoginForm(Form):
    phone = CharField(
        min_length=11,
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Телефон",
                "class": "input-field",
                "type": "text",
            }
        ),
        validators=[
            validate_phone_number,
        ],
    )

    password = CharField(
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input-field",
                "type": "password",
            }
        )
    )


class SignupForm(Form):
    first_name = CharField(
        min_length=1,
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Имя",
                "class": "input-field",
                "type": "text",
            }
        )
    )

    last_name = CharField(
        min_length=1,
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Фамилия",
                "class": "input-field",
                "type": "text",
            }
        )
    )

    phone = CharField(
        min_length=11,
        max_length=11,
        widget=TextInput(
            attrs={
                "placeholder": "Телефон",
                "class": "input-field",
                "type": "text",
            }
        ),
        validators=[
            validate_phone_number,
        ],
    )

    email = CharField(
        max_length=255,
        widget=EmailInput(
            attrs={
                "placeholder": "Почта",
                "class": "input-field",
            }
        )
    )

    password = CharField(
        max_length=255,
        widget=TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input-field",
                "type": "password",
            }
        )
    )