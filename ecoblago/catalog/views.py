from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.db.models.functions import Lower
from django.db.models import Q
from django.db.models import Prefetch

from catalog.models import Product, Region, Category, City, GalleryImage
from catalog.forms import ProductForm


class CatalogView(ListView):
    model = Product
    template_name = "catalog/catalog.html"
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = Product.objects.prefetch_related("gallery_images").all()
        self.context = self.get_context_data()

    def post(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()

    def get(self, request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
        if "action" in request.GET:
            return self.handle_ajax_get()
        return self.render_to_response(self.context)

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "add-product-to-favourites":
            return self.add_product_to_favourites()
        elif action == "remove-product-from-favourites":
            return self.remove_product_from_favourites()
        elif action == "filter-products":
            return self.get_filtered_products()

    def handle_ajax_get(self) -> JsonResponse:
        action = self.request.GET["action"]
        if action == "get-regions":
            return self.get_all_regions()
        elif action == "get-cities":
            return self.get_cities()
        elif action == "get-categories":
            return self.get_categories()

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
    
    def get_all_regions(self) -> JsonResponse:
        regions = [region.name for region in Region.objects.all()]
        return JsonResponse({"success": True, "regions": regions})

    def get_cities(self) -> JsonResponse:
        region_name = self.request.GET["region"]
        region = Region.objects.filter(name=region_name).prefetch_related("cities").first()
        if not region:
            return JsonResponse({"success": False})
        city_names = [city.name for city in region.cities.all()]
        return JsonResponse({"success": True, "cities": city_names})
    
    def get_categories(self) -> JsonResponse:
        return JsonResponse({"success": True, "categories": [category.name for category in Category.objects.all()]})

    def get_filtered_products(self) -> JsonResponse:
        search_text = self.request.POST.get("content")
        region_name = self.request.POST.get("region")
        city_name = self.request.POST.get("city")
        min_cost = int(self.request.POST.get("min-cost"))
        max_cost = int(self.request.POST.get("max-cost"))
        category_names = self.request.POST.getlist("categories[]")
        sorting_rule = self.request.POST.get("sorting-rule")

        kwargs = {}
        if region_name and city_name:
            kwargs["region__name"] = region_name
            kwargs["city__name"] = city_name

        queryset = (
            Product
            .objects
            .filter(
                description__icontains=search_text,
                cost__gte=min_cost,
                cost__lte=max_cost,
                category__name__in=category_names,
                **kwargs,
            )
            .prefetch_related("gallery_images", "liked_by")
        )

        products = []
        for product in queryset:
            dct = model_to_dict(product)
            dct["is_liked"] = self.request.user in product.liked_by.all()
            dct["main_image"] = {
                "url": product.gallery_images.all().first().image.url,
            }
            products.append(dct)

        return JsonResponse({"success": True, "products": products})

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
        self.context_ajax = {}

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
        
        self.context["categories"] = Category.objects.all()
        self.context["regions"] = Region.objects.all()
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
        gallery_images = self.request.FILES.getlist("gallery_images")
        if len(gallery_images) == 0:
            return JsonResponse({"success": False, "error": "Добавьте как минимум одну картинку"})

        form = ProductForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.seller = self.request.user
            form.save()
            for gallery_image in gallery_images:
                GalleryImage.objects.create(image=gallery_image, product=form.instance)
            return JsonResponse({"success": True})

        if len(form.errors) > 0:
            msg = list(form.errors.get_context()["errors"])[0]
            field = msg[0].capitalize()
            error = msg[1][0]
            return JsonResponse({"success": False, "error": f"{field}: {error}"})

        return JsonResponse({"success": False, "error": "Unknown error"})

    def get_cities_by_region(self) -> JsonResponse:
        region_name = self.request.POST.get("region")
        cities = get_object_or_404(Region, name=region_name).cities.all().values()
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


class ProductDetailsView(DetailView):
    models = Product
    template_name = "catalog/product_details.html"
    
    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.context = self.get_context_data()
    
    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)
    
    def get_object(self, *args, **kwargs) -> Product:
        return get_object_or_404(
            Product.objects.all()
            .select_related("region", "city", "category")
            .prefetch_related(
                "gallery_images",
            ),
            pk=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()

        context = super().get_context_data(**kwargs)
        context["image_urls"] = [image.image.url for image in self.object.gallery_images.all()]
        context["main_image_url"] = context["image_urls"][0]
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        return context
