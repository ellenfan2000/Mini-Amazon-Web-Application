# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
# from django.db.models import Q
from .backend.query import *
from .backend.request import *
from PIL import Image
import base64
# import io


def binary_to_image(large_bi):
    # data=io.BytesIO(large_bi)
    return (base64.b64encode(large_bi).decode("utf-8"))


'''
Home page to show info and recommend
'''


def get_recommentd_dic():
    recommends = get_recommend()
    re = [{"id": r.id, "name": r.name, "avg_rate": round(r.avg_rate, 2),
           "price": r.price, "img": binary_to_image(r.picture)} for r in recommends]
    return re


def home(request):
    recommends = get_recommentd_dic()
    # for p in recommends:
    #     print(p.id, p.name, p.avg_rate)
    return render(request=request, template_name="Amazon/home.html", context={"recommends": recommends})


'''
register a new user
'''


def register(request):
    if request.user.is_authenticated:
        messages.error(request, "You already are a user")
        return redirect("/")
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegForm()
    return render(request, "Amazon/register.html", {"form": form})


class UpdatePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = 'Amazon/update_password.html'
    success_url = "/"
    success_message = "Your Password Updated."


'''
updates a user's email
'''


@login_required(login_url='/login/')
def email_update(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            # form=form.save()
            user.save()
            messages.success(request, 'Your Email Address Updated.')
            return redirect("/")
    else:
        form = EmailForm()
    return render(request,
                  "Amazon/update_email.html",
                  {'form': form})


'''
Show product details
'''


@login_required(login_url='/login/')
def product_details(request, id):
    try:
        details, comments = get_product_detail(id)
        img = binary_to_image(details.picture)
    except Exception as e:
        details = None
        messages.error(request, e)
        return redirect("/")

    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            try:
                buy_product(request.user.id, id, form.cleaned_data["amount"], (
                    form.cleaned_data["address_x"], form.cleaned_data["address_y"]))
                return redirect("/order_details/"+str(id))
            except Exception as e:
                messages.error(request, e)
    form = BuyForm()
    return render(request, "Amazon/product_details.html", {"details": details, "form": form, "comments": comments, "image": img})


@login_required(login_url='/login/')
def my_orders(request):
    orders = get_all_orders(request.user.id)
    res = [{"name": o.product.name, "amount": o.amount, "cost": round(o.amount*o.product.price, 2),
            "status": o.status, "id": o.id, "img": binary_to_image(o.product.picture)} for o in orders]

    return render(request,  "Amazon/my_orders.html", {"orders": res})


@login_required(login_url='/login/')
def order_details(request, id):
    order = get_order_details(id)
    cost = round(order.Order.amount*order.Order.product.price, 2)
    img = binary_to_image(order.Order.product.picture)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                set_comments(
                    request.user.id, id, form.cleaned_data["rate"], form.cleaned_data["comment"])
                return redirect("/order_details/"+str(id))
            except:
                messages.error(
                    request, "Cannot save the change, please try again!")
        else:
            messages.error(request, "Invalid change, please try again!")
    form = FeedbackForm()
    return render(request,  "Amazon/order_details.html", {"details": order, "cost": cost, "img": img, "form": form})


@login_required(login_url='/login/')
def search_results(request):
    user_in = request.GET.get('q')
    ps = get_search_res(user_in)
    products = [{"id": p.id, "name": p.name, "category": p.category, "price": p.price,
                 "inventory": p.inventory, "img": binary_to_image(p.picture)} for p in ps]
    recommends = get_recommentd_dic()
    return render(request,  "Amazon/search_results.html", {"query": user_in, "products": products, "recommends": recommends})

@login_required(login_url='/login/')
def all_products(request):
    ps = get_all_products()
    products = [{"id": p.id, "name": p.name, "category": p.category, "price": p.price,
                 "inventory": p.inventory, "img": binary_to_image(p.picture)} for p in ps]
    return render(request,  "Amazon/all_products.html", {"products": products})