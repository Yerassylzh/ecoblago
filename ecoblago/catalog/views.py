from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse

from catalog.models import Product, Region
from catalog.forms import ProductForm


class CatalogView(ListView):
    model = Product
    template_name = "catalog/catalog.html"
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax()

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def handle_ajax(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "add-product-to-favourites":
            return self.add_product_to_favourites()
        elif action == "remove-product-from-favourites":
            return self.remove_product_from_favourites()

    def add_product_to_favourites(self) -> JsonResponse:
        product_id = self.request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        self.request.user.liked_products.add(product)
        return JsonResponse({"success": True})

    def remove_product_from_favourites(self) -> JsonResponse:
        product_id = self.request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        self.request.user.liked_products.remove(product)
        return JsonResponse({"success": True})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        context["liked_products"] = self.request.user.liked_products.all()

        return context


class CreateProductView(TemplateView):
    template_name = "catalog/create_product.html"

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

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.GET:
            return self.handle_ajax_get()
        return self.render_to_response(self.context)

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "create-product":
            return self.create_product()
        elif action == "get-cities-by-region":
            return self.get_cities_by_region()

    def handle_ajax_get(self) -> JsonResponse:
        pass

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

    def get_cities_by_region(self) -> JsonResponse:
        return JsonResponse({"success": True, "cities": ["Taldykorgan", "Almaty"]})

        region = self.request.POST.get("region")
        cities = get_object_or_404(Region, name=region).cities.all()
        cities = cities.values_list("name", flat=True)
        self.context_ajax["success"] = True
        self.context_ajax["cities"] = list(cities)
        return JsonResponse(data=self.context_ajax)


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
