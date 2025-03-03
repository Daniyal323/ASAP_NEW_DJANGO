from django.shortcuts import redirect, render
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address
from django.db.models import Avg, Count
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.
def index(request):
    #products = Product.objects.all()
    products = Product.objects.filter(featured = True)

    context = {
        'products': products
    }

    return render(request, 'core/index.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    return render(request, 'core/contact.html')

def product_list_view(request):
    products = Product.objects.filter(product_status="publised")
    #products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories" : categories
    }

    return render(request, 'core/categories-list.html', context)


def category_product_list_view(request,cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status ="publised", category=category)

    context = {
        'category': category,
        'products':products,
    }
    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors
    }
    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status ="publised")
    context = {
        "vendor": vendor,
        "products": products,
    }

    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_images.all()

    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    #Getting Reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #Service Review Form
    review_form = ProductReviewForm()

    context = {
        "p":product,
        "p_image": p_image,
        "products": products,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_form": review_form,
    }
    return render(request, "core/product-detail.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews,
        }
    )

def search_view(request):
    service_title = request.GET.get("title", "").strip()
    city = request.GET.get("city", "").strip()

    # Start with an empty query
    products = Product.objects.all()

    # Filter by title if provided
    if service_title:
        products = products.filter(title__icontains=service_title)

    # Filter by city if provided
    if city:
        products = products.filter(city__icontains=city)

    context = {
        "products": products.order_by("-date"),
        "service_title": service_title,
        "city": city,
    }

    return render(request, "core/search.html", context)


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.session['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else: 
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session: 
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET["id"])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session: 
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def save_checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method =="POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['address'] = address
        request.session['mobile'] = mobile
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country

        if 'cart_data_obj' in request.session: 
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])

            order = CartOrder.objects.create(
                user = request.user,
                price = total_amount,
                full_name = full_name,
                email = email,
                address = address,
                phone = mobile,
                city = city,
                state = state,
                country = country,
            )

            del request.session['full_name']
            del request.session['email'] 
            del request.session['address']
            del request.session['mobile']  
            del request.session['city'] 
            del request.session['state'] 
            del request.session['country']

            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                card_order_products = CartOrderItems.objects.create(
                    order = order,
                    invoice_no = "INVOICE_NO-" + str(order.id),
                    item = item['title'],
                    image = item['image'],
                    qty = item['qty'],
                    price = item['price'],
                    total = float(item['qty']) * float(item['price'])
                )
        return redirect("core:checkout", order.oid)
    return redirect("core:checkout", order.oid)

def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    context ={
        "order": order,
        "order_items": order_items,
    }
    return render(request, "core/checkout.html", context)

# @login_required
# def checkout_view(request):
#     cart_total_amount = 0
#     total_amount = 0
#     if 'cart_data_obj' in request.session: 
#         for p_id, item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float(item['price'])

#         order = CartOrder.objects.create(
#             user = request.user,
#             price = total_amount,
#         )

#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])

#             card_order_products = CartOrderItems.objects.create(
#                 order = order,
#                 invoice_no = "INVOICE_NO-" + str(order.id),
#                 item = item['title'],
#                 image = item['image'],
#                 qty = item['qty'],
#                 price = item['price'],
#                 total = float(item['qty']) * float(item['price'])
#             )

#     host = request.get_host()
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': cart_total_amount,
#         'item_name': "Order-item-No-" + str(order.id),
#         'invoice': "INVOICE_No-"+ str(order.id),
#         'currency_code': "USD",
#         'notify_url': 'http:/{}{}'.format(host, reverse("core:paypal-ipn")),
#         'return_url': 'http:/{}{}'.format(host, reverse("core:payment-completed")),
#         'cancel_url': 'http:/{}{}'.format(host, reverse("core:payment-failed")),
#     }

#     paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session: 
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
   
#     return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'paypal_payment_button': paypal_payment_button})

@login_required   
def payment_completed_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status == True
        order.save()

    context = {
        "order": order,
    }
    return render(request, "core/payment-completed.html", context)

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')
