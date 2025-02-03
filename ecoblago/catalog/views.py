from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse

from authpage.models import User


class CatalogView(TemplateView):
    template_name = "catalog/catalog.html"
    
    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context = self.get_context_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_logined"] = ("remembered" in self.request.session)
        context["my_user"] = get_object_or_404(User.objects, username=self.request.session.get("username"))
        context["theme"] = (self.request.COOKIES["theme"] if "theme" in self.request.COOKIES else "light")

        return context
