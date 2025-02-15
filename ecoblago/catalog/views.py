from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse

from catalog.models import Product
from catalog.forms import ProductForm


class CatalogView(ListView):
    model = Product
    template_name = "catalog/catalog.html"
    
    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        pass

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")

        return context

class CreateProductView(TemplateView):
    template_name = "catalog/create_product.html"

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax()

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def handle_ajax(self) -> JsonResponse:
        if self.request.POST.get("action") == "create-product":
            return self.create_product()

    def create_product(self) -> JsonResponse:
        form = ProductForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.seller = self.request.user
            form.save()
            return JsonResponse({"success": True})

        if len(form.errors) > 0:
            msg = list(form.errors.get_context()["errors"])[0]
            field = msg[0].capitalize()
            error = msg[1][0]
            return JsonResponse({"success": False, "error": f"{field}: {error}"})

        return JsonResponse({"success": False, "error": "Unknown error"})

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context = self.get_context_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        context["form"] = ProductForm()
        context["my_user"] = self.request.user

        return context


class MyProductsView(ListView):
    model = Product
    template_name = "catalog/my_products.html"

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")

        return context