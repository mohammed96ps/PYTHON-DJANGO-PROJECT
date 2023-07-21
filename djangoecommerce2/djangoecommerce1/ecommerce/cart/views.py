from django.shortcuts import render,redirect
from shop.models import Category,Product
from cart.models import Cart
from django.contrib.auth.decorators import login_required

@login_required()
def add_cart(request,p):
    product=Product.objects.get(id=p)
    user=request.user
    try:
        cart=Cart.objects.get(products=product,user=user)
        if cart.quantity<cart.products.stock:
            cart.quantity+=1
        cart.save()

    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=user,products=product,quantity=1)
        cart.save()
    return redirect('cart:cartview')

@login_required()
def cartview(request):
    total=0
    user=request.user
    try:
        cart=Cart.objects.filter(user=user)
        for i in cart:
            total+=i.quantity*i.products.price
    except Cart.DoesNotExist:
        pass

    return render(request,'cart.html',{'cart':cart,'total':total})

@login_required()
def less_cart(request,p):
    product = Product.objects.get(id=p)
    user = request.user
    try:
        cart = Cart.objects.get(products=product, user=user)
        if cart.quantity>1:
            cart.quantity -= 1
            cart.save()
        else:

            cart.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart:cartview')

@login_required()
def delete_cart(request,p):
    product = Product.objects.get(id=p)
    user = request.user
    try:
        cart = Cart.objects.get(products=product, user=user)
        cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')
