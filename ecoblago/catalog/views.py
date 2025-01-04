from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse

from authpage.models import User


class CatalogView(View):
    template_url = "catalog/catalog.html"
    
    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        context = {
            "my_user": get_object_or_404(User.objects, username=request.session.get("username")),
            "user_logined": ("remembered" in self.request.session),
        }

        return render(request, self.template_url, context=context)
