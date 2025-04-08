from typing import Union
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseForbidden,
)
from django.db.models import Q
from django.core.files import File
from django.utils.translation import gettext as _
from PIL import Image

from catalog.models import Product, Region, Category, GalleryImage
from catalog.forms import ProductForm
from core.utils import get_cropped_image

class CatalogView(ListView):
    model = Product
    template_name = "catalog/catalog.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def get_queryset(self):
        return (
            Product
            .objects
            .prefetch_related(
                "gallery_images",
            )
            .only("id", "title", "cost")
        )

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
        if action == "remove-product-from-favourites":
            return self.remove_product_from_favourites()
        if action == "filter-products":
            return self.get_filtered_products()

    def handle_ajax_get(self) -> JsonResponse:
        action = self.request.GET["action"]
        if action == "get-regions":
            return self.get_all_regions()
        if action == "get-cities":
            return self.get_cities()
        if action == "get-categories":
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
        region = (
            Region
            .objects
            .filter(name=region_name)
            .prefetch_related("cities")
            .first()
        )
        if not region:
            return JsonResponse({"success": False})
        city_names = [city.name for city in region.cities.all()]
        return JsonResponse({"success": True, "cities": city_names})

    def get_categories(self) -> JsonResponse:
        return JsonResponse({
            "success": True,
            "categories": [
                category.name for category in Category.objects.all()
            ]
        })

    def get_filtered_products(self) -> JsonResponse:
        search_text = self.request.POST.get("content").strip()
        region_name = self.request.POST.get("region").strip()
        city_name = self.request.POST.get("city").strip()
        min_cost = int(self.request.POST.get("min-cost"))
        max_cost = int(self.request.POST.get("max-cost"))
        category_names = self.request.POST.getlist("categories[]")

        kwargs = {}
        args = []
        if region_name and city_name:
            kwargs["region__name"] = region_name
            kwargs["city__name"] = city_name

        if len(search_text) > 0:
            args.append(
                Q(description__icontains=search_text)
                | Q(title__icontains=search_text)
            )

        if len(category_names) > 0:
            kwargs["category__name__in"] = category_names

        queryset = (
            self
            .object_list
            .filter(
                *args,
                cost__gte=min_cost,
                cost__lte=max_cost,
                **kwargs,
            )
        )

        products = []
        for product in queryset:
            dct = {
                "is_liked": product in self.context["liked_products"],
                "title": product.title,
                "cost": product.cost,
                "main_image": {
                    "url": product.gallery_images.all()[0].image.url,
                },
                "id": product.pk,
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
        if action == "get-cities-by-region":
            return self.get_cities_by_region()

    def handle_ajax_get(self) -> JsonResponse:
        pass

    def create_product(self) -> JsonResponse:
        gallery_images = self.request.FILES.getlist("gallery_images")
        if len(gallery_images) == 0:
            return JsonResponse({
                "success": False,
                "error": _("Добавьте как минимум одну картинку")
            })

        form = ProductForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.seller = self.request.user
            form.save()

            gallery_images_list = []
            
            for image in gallery_images:
                # Open and crop the image
                img = Image.open(image)
                cropped_img = get_cropped_image(img, 4/3)
                                
                temp_file = BytesIO()
                cropped_img.save(temp_file, format=img.format or 'JPEG')
                temp_file.seek(0)
                
                cropped_file = File(temp_file, name=image.name)
                
                gallery_images_list.append(
                    GalleryImage(
                        image=cropped_file,
                        product=form.instance
                    )
                )

            GalleryImage.objects.bulk_create(gallery_images_list)
            return JsonResponse({"success": True})

        if len(form.errors) > 0:
            msg = list(form.errors.get_context()["errors"])[0]
            field = msg[0].capitalize()
            error = msg[1][0]
            return JsonResponse({
                "success": False,
                "error": f"{field}: {error}"
            })

        return JsonResponse({"success": False, "error": _("Unknown error")})

    def get_cities_by_region(self) -> JsonResponse:
        region_name = self.request.POST.get("region")
        cities = get_object_or_404(Region, name=region_name).cities.all()
        self.context_ajax["success"] = True
        self.context_ajax["cities"] = [city.name for city in cities]
        return JsonResponse(data=self.context_ajax)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        context["form"] = ProductForm()
        context["my_user"] = self.request.user
        context["categories"] = [
            category.name for category in Category.objects.all()
        ]
        context["regions"] = [region.name for region in Region.objects.all()]

        return context


class MyProductsView(ListView):
    model = Product
    template_name = "catalog/my_products.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST["action"]
        if action == "filter-products":
            return self.get_filtered_products()

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def get_filtered_products(self) -> JsonResponse:
        search_text = self.request.POST.get("content").strip()
        region_name = self.request.POST.get("region").strip()
        city_name = self.request.POST.get("city").strip()
        min_cost = int(self.request.POST.get("min-cost"))
        max_cost = int(self.request.POST.get("max-cost"))
        category_names = self.request.POST.getlist("categories[]")

        kwargs = {}
        args = []
        if region_name and city_name:
            kwargs["region__name"] = region_name
            kwargs["city__name"] = city_name

        if len(search_text) > 0:
            args.append(
                Q(description__icontains=search_text)
                | Q(title__icontains=search_text)
            )

        if len(category_names) > 0:
            kwargs["category__name__in"] = category_names

        queryset = (
            self
            .object_list
            .filter(
                *args,
                cost__gte=min_cost,
                cost__lte=max_cost,
                **kwargs,
            )
        )

        products = []
        for product in queryset:
            dct = {
                "is_liked": product in self.context["liked_products"],
                "title": product.title,
                "cost": product.cost,
                "main_image": {
                    "url": product.gallery_images.all()[0].image.url,
                },
                "id": product.pk,
            }
            products.append(dct)

        return JsonResponse({"success": True, "products": products})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_products"] = self.request.user.liked_products.all()
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

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "delete":
            return self.delete_product()

    def delete_product(self) -> JsonResponse:
        if self.object.seller != self.request.user:
            return JsonResponse({
                "success": False,
                "error": _("You are not the seller of this product")
            })
        self.object.delete()
        return JsonResponse({"success": True})

    def get_object(self, *args, **kwargs) -> Product:
        return get_object_or_404(
            Product.objects.all()
            .select_related("region", "city", "category")
            .prefetch_related(
                "gallery_images",
            ),
            pk=self.kwargs["pk"]
        )

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object(*args, **kwargs)

        context = super().get_context_data(**kwargs)
        context["image_urls"] = [
            image.image.url for image in self.object.gallery_images.all()
        ]
        context["main_image_url"] = context["image_urls"][0]
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")

        return context


class EditProductView(DetailView):
    models = Product
    template_name = "catalog/edit_product.html"

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.context = self.get_context_data()

        if self.object.seller != self.request.user:
            return HttpResponseForbidden(
                "You are not the seller of this product"
            )

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "edit":
            return self.edit_product()

    def edit_product(self) -> JsonResponse:
        gallery_images = self.request.FILES.getlist("gallery_images")
        if len(gallery_images) == 0:
            return JsonResponse({
                "success": False,
                "error": _("Добавьте как минимум одну картинку")
            })

        form = ProductForm(
            self.request.POST,
            self.request.FILES,
            instance=self.object
        )
        if form.is_valid():
            form.save()
            self.object.gallery_images.all().delete()

            gallery_images_list = []            
            for image in gallery_images:
                img = Image.open(image)
                cropped_img = get_cropped_image(img, 4/3)
                                
                temp_file = BytesIO()
                cropped_img.save(temp_file, format=img.format or 'JPEG')
                temp_file.seek(0)
                
                cropped_file = File(temp_file, name=image.name)
                
                gallery_images_list.append(
                    GalleryImage(
                        image=cropped_file,
                        product=form.instance
                    )
                )

            GalleryImage.objects.bulk_create(gallery_images_list)
            return JsonResponse({"success": True})

        if len(form.errors) > 0:
            msg = list(form.errors.get_context()["errors"])[0]
            field = msg[0].capitalize()
            error = msg[1][0]
            return JsonResponse({
                "success": False,
                "error": f"{field}: {error}"
            })

        return JsonResponse({"success": False, "error": _("Unknown error")})

    def get_object(self, *args, **kwargs) -> Product:
        return get_object_or_404(
            Product.objects.all()
            .select_related("region", "city", "category")
            .prefetch_related(
                "gallery_images",
            ),
            pk=self.kwargs["pk"]
        )

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object(*args, **kwargs)

        context = super().get_context_data(**kwargs)
        context["image_urls"] = [
            image.image.url for image in self.object.gallery_images.all()
        ]
        context["main_image_url"] = context["image_urls"][0]
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")

        context["title"] = self.object.title
        context["cost"] = self.object.cost
        context["category"] = self.object.category.name
        context["description"] = self.object.description
        context["region"] = self.object.region
        context["phone-number"] = self.object.phone_number
        context["email"] = self.object.email
        context["image_urls"] = [
            image.image.url for image in self.object.gallery_images.all()
        ]

        context["categories"] = [
            category.name for category in Category.objects.all()
        ]
        context["regions"] = [region.name for region in Region.objects.all()]

        return context


class LikedProductsView(ListView):
    model = Product
    template_name = "catalog/liked_products.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_queryset()
        self.context = self.get_context_data()

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.GET:
            return self.handle_ajax_get()
        return self.render_to_response(self.context)
    
    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if "action" in self.request.POST:
            return self.handle_ajax_post()
    
    def handle_ajax_get(self) -> JsonResponse:
        pass
    
    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST["action"]
        if action == "filter-products":
            return self.get_filtered_products()

    def get_queryset(self):
        return (
            self.request.user.liked_products
            .prefetch_related("gallery_images")
            .only("id", "title", "cost")
        )

    def get_filtered_products(self) -> JsonResponse:
        search_text = self.request.POST.get("content").strip()
        region_name = self.request.POST.get("region").strip()
        city_name = self.request.POST.get("city").strip()
        min_cost = int(self.request.POST.get("min-cost"))
        max_cost = int(self.request.POST.get("max-cost"))
        category_names = self.request.POST.getlist("categories[]")

        kwargs = {}
        args = []
        if region_name and city_name:
            kwargs["region__name"] = region_name
            kwargs["city__name"] = city_name

        if len(search_text) > 0:
            args.append(
                Q(description__icontains=search_text)
                | Q(title__icontains=search_text)
            )

        if len(category_names) > 0:
            kwargs["category__name__in"] = category_names

        queryset = (
            self
            .object_list
            .filter(
                *args,
                cost__gte=min_cost,
                cost__lte=max_cost,
                **kwargs,
            )
        )

        products = []
        for product in queryset:
            dct = {
                "is_liked": product in self.context["liked_products"],
                "title": product.title,
                "cost": product.cost,
                "main_image": {
                    "url": product.gallery_images.all()[0].image.url,
                },
                "id": product.pk,
            }
            products.append(dct)

        return JsonResponse({"success": True, "products": products})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_products"] = self.request.user.liked_products.all()
        context["my_user"] = self.request.user
        context["theme"] = self.request.COOKIES.get("theme", "light")
        context["lang"] = self.request.COOKIES.get("lang", "ru")
        return context
