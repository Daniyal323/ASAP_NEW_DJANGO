from django.urls import include, path
from core.views import index, product_list_view,product_detail_view, category_list_view, category_product_list_view, vendor_list_view, vendor_detail_view,ajax_add_review, search_view,add_to_cart, cart_view,delete_item_from_cart, checkout, payment_completed_view, payment_failed_view
from core import views

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    path('services/', product_list_view, name="service-list"),
    path('service/<pid>/', product_detail_view, name="service-detail"),

    path('category/', category_list_view, name="category"),
    path('category-product/<cid>', category_product_list_view, name="category-product-list"),

    path('vendors/', vendor_list_view, name="vendor-list"),
    path('vendor/<vid>/', vendor_detail_view, name="vendor-detail"),

    path('ajax-add-review/<int:pid>/', ajax_add_review, name="ajax-add-review"),

    path('search/', search_view, name="search"),

    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    path('cart/', cart_view, name="cart"),

    path('delete-from-cart/', delete_item_from_cart, name="delete-from-cart"),

    path('checkout/<oid>/', checkout, name="checkout"),

    path('paypal/', include('paypal.standard.ipn.urls')),

    path('payment-completed/<oid>/', payment_completed_view, name="payment-completed"),

    path('payment-failed/', payment_failed_view, name="payment-failed"),

    path('save_checkout_view/',views.save_checkout_view, name="save_checkout_view")
]