from typing import Union

from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse


class CatalogView(View):
    template_url = "catalog/catalog.html"
    
    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        return render(request, self.template_url)
