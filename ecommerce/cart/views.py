from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart

from cart.models import Account


# Create your views here.

def cartview(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total += i.quantity * i.product.price
    return render(request, "cartview.html", {'c': cart, 't': total})


def addtocart(request, n):
    p = Product.objects.get(name=n)
    u = request.user  # current login user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if (cart.quantity < cart.product.stock):
            cart.quantity += 1
            cart.save()
    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
    return cartview(request)


def cart_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user  # current login user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return cartview(request)


def full_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user  # current login user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
    except:
        pass
    return cartview(request)


def orderform(request):
    if (request.method == "POST"):
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']
        u = request.user
        cart = Cart.objects.filter(user=u)

        total = 0
        for i in cart:
            total += i.quantity * i.product.price

            try:
                num = int(n)
                ac = Account.objects.get(acctnum=n)
                if (ac.amount >= total):
                    ac.amount = ac.amount - total
                    ac.save()
                    return HttpResponse("Ordered")
                else:
                    return HttpResponse("Insufficient Fund")
            except:
                pass

    return render(request, "orderform.html")
