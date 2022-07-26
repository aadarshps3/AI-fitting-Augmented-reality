from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.utils import timezone
import cv2
from django.http import JsonResponse
import Shirt as s

from .forms import ReviewForm, CheckoutForm, PaymentForm, CustomerForm, ComplaintForm
from .models import *



def user_home(request):
    return render(request, 'user_panel/user_home.html')

def user_profile(request):
    # u = request.user
    profile = Customer.objects.filter(username=request.user)
    return render(request, 'user_panel/user_profile.html', {'profile': profile})


def profile_update(request, id):
    a = Customer.objects.get(id=id)
    if request.method == "POST":
        form = CustomerForm(request.POST or None, instance=a)
        if form.is_valid():
            form.save()
            messages.info(request, 'updated sucessfully')
            return redirect('user_profile')
    else:
        form = CustomerForm(instance=a)
    return render(request, 'user_panel/user_profile_update.html', {'form': form})


def user_product_view(request):
    p = product.objects.all()
    return render(request, 'user_panel/user_product_view.html', {'p': p})

@login_required
def product_detail(request, id):
    review = Review.objects.filter(item=id)
    reviews_count = Review.objects.filter(item=id).count()
    form = ReviewForm()
    obj = product.objects.filter(id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            re = form.save(commit=False)
            re.customer = request.user
            re.item = product.objects.get(id=id)
            re.save()
            return redirect('product_detail', id)

    return render(request, 'user_panel/detail.html',
                  {'data': obj, 'form': form, 'review': review, 'reviews_count': reviews_count})



@login_required
def cart(request):
    try:

        order = Order.objects.get(customer=request.user, ordered=False)
        context = {
            'object': order
        }
        return render(request, 'user_panel/cart.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("user_home")


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(product, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item_id=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(customer=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart", )


        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart", )
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart", )


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user.customer,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart", )
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart", )

@login_required
def checkout(request, id):
    user = request.user,
    orders = Order.objects.get(id=id)

    addressform = CheckoutForm()
    if request.method == 'POST':
        addressform = CheckoutForm(request.POST)
        if addressform.is_valid():
            address = addressform.save(commit=False)
            address.customer = request.user
            addressform.save()

            orders.shipping_address = address
            orders.save()
            return redirect('payment', id)

    return render(request, 'user_panel/checkout.html', {
        'form': addressform,
        'object': orders,

    })

@login_required
def payment(request, id):
    user = request.user,
    order = Order.objects.get(id=id)
    cart_total = order.get_total()

    payment_form = PaymentForm()

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            pay = payment_form.save(commit=False)
            pay.customer = request.user
            pay.amount = cart_total
            payment_form.save()
            order.ordered = True
            order.ordered_date = timezone.now()
            order.payment = pay
            order.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()





            messages.info(request, 'Congratulations!! Your Order Placed Successfully')
            return redirect('order_status')
    return render(request, 'user_panel/payment.html', {
        'form': payment_form,
        'object': order,

    })

@login_required
def order_status(request):
    customer = request.user
    order = Order.objects.filter(customer=customer, ordered=True)
    return render(request, 'user_panel/orders.html', {'orders': order})
# Complaint
def complaint_add_user(request):
    form = ComplaintForm()
    u = request.user
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successful')
            return redirect('user_home')

    return render(request, 'user_panel/user_add_complaint.html', {'form': form})


def complaint_view_user(request):
    n = Complaint.objects.filter(user=request.user)
    return render(request, 'user_panel/user_view_complaint.html', {'n': n})



def a(request):
    # if request.method == "POST":
    #     obj = product.objects.all().last()
    #     # scr = obj.image1
    #     classify_file = 'media/products/' + str(obj)
    #     print(classify_file)
        s.run("503.jpg")
        return redirect('user_product_view')



