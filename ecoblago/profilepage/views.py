from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpRequest, HttpResponse, JsonResponse

from authpage.models import User

from django.contrib.auth.models import AbstractUser 


class ProfilepageView(DetailView):
    model = User
    template_name = "profilepage/profilepage.html"
    context_object_name = "user"
    pk_url_kwarg = "pk"

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        self.context.update({
            "change_allowed": self.request.session.get("username") == self.object.username,
            "input_fields": [
                {
                    "title": "Имя",
                    "icon_class": "fas fa-user",
                    "content": self.object.first_name,
                },
                {
                    "title": "Фамилия",
                    "icon_class": "fas fa-user",
                    "content": self.object.last_name,
                },
                {
                    "title": "Номер телефона",
                    "icon_class": "fas fa-phone",
                    "content": self.object.phone_number,
                },
                {
                    "title": "Электронная почта",
                    "icon_class": "fas fa-envelope",
                    "content": self.object.email,
                },
            ],
            "about": {
                "content": self.object.about,
            },
        })

        return self.render_to_response(self.context)    

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)

        self.object = self.get_object()
        self.context = self.get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user_id"] = kwargs["pk"]
        return context
