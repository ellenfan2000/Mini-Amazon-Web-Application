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

'''
Home page to show info and recommend
'''


def home(request):
    recommends = get_recommend()
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
        details = get_product_detail(id)
    except:
        details = None
        messages.error(request, "The prodcut you queried does not exist")
        return redirect("/")
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            try:
                buy_product(request.user.id, id, form.cleaned_data["amount"], (
                    form.cleaned_data["address_x"], form.cleaned_data["address_y"]))
            except:
                messages.error(request, "The operation is invalid, please try again!")
    form = BuyForm()
    return render(request, "Amazon/product_details.html", {"details": details,"form":form})

@login_required(login_url='/login/')
def my_orders(request):
    orders = get_all_orders(request.user.id)
    return render(request,  "Amazon/my_orders.html",{"orders":orders})

@login_required(login_url='/login/')
def order_details(request,id):
    order = get_product_detail(id)
    return render(request,  "Amazon/order_details.html",{"details":order})