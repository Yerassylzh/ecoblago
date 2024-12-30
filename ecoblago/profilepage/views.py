from typing import Union

from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse

from authpage.models import User


class ProfilepageView(View):
    template_url = "profilepage/profilepage.html"
    
    def setup(self, request, *args, **kwargs):
        self.pk = kwargs.get("pk")
        return super().setup(request, *args, **kwargs)

    def post(self, request: HttpRequest, **kwargs) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, request: HttpRequest, **kwargs) -> Union[HttpResponse, JsonResponse]:
        user = User.objects.get(pk=self.pk)
        context = {
            "change_allowed": request.session.get("username") == user.username,
            "input_fields": [
                {
                    "title": "Имя",
                    "icon_class": "fas fa-user",
                    "content": user.name,
                },
                {
                    "title": "Фамилия",
                    "icon_class": "fas fa-user",
                    "content": user.surname,
                },
                {
                    "title": "Номер телефона",
                    "icon_class": "fas fa-phone",
                    "content": user.phone_number,
                },
                {
                    "title": "Электронная почта",
                    "icon_class": "fas fa-envelope",
                    "content": user.email,
                },
            ],
            "about": {
                "content": user.about,
            },
        }

        return render(request, self.template_url, context=context)
