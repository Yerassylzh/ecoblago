from django.forms import ValidationError


def validate_phone_number(phone_number: str):
    phone_number = "".join(
        list(
            filter(
                lambda c: "0" <= c <= "9",
                phone_number,
            ),
        ),
    )

    if len(phone_number) != 11:
        raise ValidationError(
            f"Длинна номера телефона должна быть 11. Но вы ввели: '{phone_number}'."
        )
    
    if phone_number[0] != "7":
        raise ValidationError(
            f"Номер телефона должен начинатся с 7. Но вы ввели: '{phone_number}'."
        )
