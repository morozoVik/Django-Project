from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ProductDetailView, CategoriesView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoriesView.as_view(), name="categories"),
]
