from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("create", views.CreateProductView.as_view(), name="create"),
    path("my_products", views.MyProductsView.as_view(), name="my_products"),
    path("product_details/<int:pk>", views.ProductDetailsView.as_view(), name="product_details"),
    path("edit/<int:pk>", views.EditProductView.as_view(), name="edit"),
]
