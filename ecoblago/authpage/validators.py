from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class PhoneNumberValidator:
    def __call__(self, number: str):
        chrs = list(filter(lambda c: c != ' ', number))
        if chrs[0] == '+':
            chrs.pop(0)

        if not "".join(chrs).isnumeric():
            raise ValidationError("Номер телефона содержит лишние символы")
    
        if len(chrs) > 11:
            raise ValidationError("Номер телефона слишком длинный")
        
        if len(chrs) < 11:
            raise ValidationError("Номер телефона слишком короткий")

        if chrs[0] not in '78':
            raise ValidationError(f"Номер телефона не может начинатся на '{chrs[0]}'")
