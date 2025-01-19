from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("add-products/", views.add_product, name="add_products"),
    path("edit-products/<pid>/", views.edit_product, name="edit_products"),
    path("delete-products/<pid>/", views.delete_product, name="delete_products"),
    path("orders/", views.orders, name="orders"),
    path("order-details/<id>/", views.order_detail, name="order_detail"),
    path("change_order_status/<oid>/", views.change_order_status, name="change_order_status"),

]