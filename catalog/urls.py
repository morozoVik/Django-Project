from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, CategoriesView, ContactsView,
    unpublish_product, change_product_status
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("product/<int:pk>/unpublish/", unpublish_product, name="product_unpublish"),
    path("product/<int:pk>/status/<str:status>/", change_product_status, name="change_product_status"),
]