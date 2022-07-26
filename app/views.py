from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from app.filters import OrderFilter
from app.forms import CustomerForm,ProductForm
from app.models import product, Customer, Order, Complaint


def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("uname")
        password = request.POST.get("pass")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user.is_user:
                return redirect('user_home')
            else:
                return redirect('login_view')
        else:
            messages.info(request, "invalid")
            return redirect(login_view)
    return render(request, 'login.html')


def admin_home(request):
    return render(request, 'admin_panel/admin_home.html')


def register(request):

    customerform = CustomerForm()
    if request.method == 'POST':

        customerform = CustomerForm(request.POST)
        if customerform.is_valid():
            user = customerform.save(commit=False)
            user.is_user = True
            user.save()
            c = customerform.save(commit=False)
            c.user = user
            c.save()
            messages.info(request, 'Registered Successfully')
            return redirect('login_view')
    return render(request, 'register.html', {'customerform': customerform})

@login_required
def user_view(request):
    customer = Customer.objects.all()
    return render(request, 'admin_panel/user_view.html', {'customer': customer})
@login_required
def delete_user(request, id):
    data = Customer.objects.get(id=id)
    if request.method=='POST':
        data.delete()
    return redirect('user_view')

@login_required
def product_add(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'product added successful')
            return redirect('product_view')
    return render(request, 'admin_panel/product_add.html', {'form': form})

@login_required
def product_view(request):
    p = product.objects.all()
    return render(request, 'admin_panel/product_view.html', {'p': p})

@login_required
def update_product(request, id):
    data = product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form = ProductForm(request.POST or None, instance=data)
    return render(request,'admin_panel/product_update.html', {'form': form})


@login_required
def delete_product(request, id):
    data = product.objects.get(id=id)
    if request.method=='POST':
        data.delete()
    return redirect('product_view')

@login_required
def view_orders_admin(request):
    data = Order.objects.filter(ordered=True)
    orderFilter = OrderFilter(request.GET, queryset=data)
    data = orderFilter.qs
    context = {
        'data': data,
        'orderFilter': orderFilter,
    }
    return render(request, 'admin_panel/orders.html', context)

@login_required
def view_payment(request):
    work = Order.objects.filter(ordered=True)
    orderFilter = OrderFilter(request.GET, queryset=work)
    work = orderFilter.qs
    context = {
        'data': work,
        'orderFilter': orderFilter,
    }
    return render(request, 'admin_panel/view_payment_details.html', context)

@login_required
def delivery_detail(request):
    work = Order.objects.filter(ordered=True)
    orderFilter = OrderFilter(request.GET, queryset=work)
    work = orderFilter.qs
    context = {
        'data': work,
        'orderFilter': orderFilter,
    }
    return render(request, 'admin_panel/delivery.html', context)


@login_required
def complete_delivery(request, id):
    order = Order.objects.get(id=id)
    order.completed = True
    order.completed_date = datetime.now()
    order.save()
    messages.info(request, 'Order Completed Successfully')
    return redirect('delivery_detail')

def complaint_view(request):
    c = Complaint.objects.all()
    return render(request, 'admin_panel/complaint_view.html', {'c': c})


def reply_complaint(request, id):
    c = Complaint.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        c.reply = r
        c.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('complaint_view')
    return render(request, 'admin_panel/reply_complaint.html', {'c': c})



def logout_view(request):
    logout(request)
    return redirect('login_view')



