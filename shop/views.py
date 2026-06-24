from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            name__icontains=query
        )
    else:
        products = Product.objects.all()

    return render(request, 'index.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {
        'product': product
 })

def cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    return render(request, 'cart.html', {
        'products': products
    })
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', [])
    cart.append(product.id)
    request.session['cart'] = cart

    return redirect('cart')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

def checkout(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        Order.objects.create(
            user=request.user,
            total_amount=product.price
        )

    return render(request, 'success.html', {
        'total': product.price,
        'product': product
    })

def remove_from_cart(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id)

    request.session['cart'] = cart

    return redirect('cart')