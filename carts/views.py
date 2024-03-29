#
#   file 	: carts/views.py
#	author	: andromeda
#   desc 	: Model parsing and variable retrieval for each carts app URL controller
#

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Cart

def cart_home(request):
    cart_id = request.session.get("cart_id", None)
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        cart_obj = qs.first()
        if request.user.is_authenticated() and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.objects.new(user=request.user)
        request.session['cart_id'] = cart_obj.id
    return render(request, "carts/home.html", {})
