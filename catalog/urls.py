from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import categories, contacts, home, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("categories/", categories, name="categories"),
]
