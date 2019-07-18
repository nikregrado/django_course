from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from polls.models import Category, Game, Order, Cart, Key
from polls.forms import  OrderForm, RegistrationForm, LoginForm
from random import randint


def index(request):
    if not request.session.session_key:
        request.session.create()
        print("if not", request.session.session_key)
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        print("else", request.session.session_key)
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    categories = Category.objects.all()
    games = Game.objects.all()
    context = {
        'categories': categories,
        'games': games,
        'cart_size': cart_size
    }
    return render(request, 'base.html', context)


def game_view(request, game_slug):
    if not request.session.session_key:
        request.session.create()
        print(request.session.session_key)
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        print(request.session.session_key)
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    game = Game.objects.get(slug=game_slug)
    categories = Category.objects.all()
    context = {
        'game': game,
        'categories': categories,
        'cart_size': cart_size
    }
    return render(request, 'game.html', context)


def category_view(request, category_slug):
    if not request.session.session_key:
        request.session.create()
        print(request.session.session_key)
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        print(request.session.session_key)
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    category = Category.objects.get(slug=category_slug)
    game_category = Game.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'game_category': game_category,
        'categories': categories
    }
    return render(request, 'category.html', context)


def cart_view(request):
    if not request.session.session_key:
        request.session.create()
        print(request.session.session_key)
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        print(request.session.session_key)
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    new_item_cost = 0.00
    for product in request.session['cart']:
        new_item_cost += round(float(product['total']), 2)
    context = {
        'cart': cart,
        'cart_size': cart_size,
        'cart_cost': new_item_cost,
    }
    request.session['cart_cost'] = 0
    for product in request.session['cart']:
        request.session['cart_cost'] += product['total']
    return render(request, 'cart.html', context)

def cart_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    new_item_cost = 0.00
    for product in request.session['cart']:
        new_item_cost += round(float(product['total']), 2)
    context = {
        'carts': cart,
        'cart_size': cart_size,
        'cart_cost': new_item_cost,
    }
    request.session['cart_cost'] = 0
    for product in request.session['cart']:
        request.session['cart_cost'] += product['total']
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']

    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    product_slug = request.GET.get('game_slug')
    product = Game.objects.get(slug=product_slug)
    # is_in = False
    # for prd in request.session['cart']:
    #     if prd['id'] == product.id:
    #         is_in = True
    # if not is_in:
    request.session['cart_size'] += 1
    request.session['cart_id'] += 1
    request.session['cart'].append({'cart_id': request.session['cart_id'],
                                        'id': product.id,
                                        'name': product.title,
                                        'price': round(float(product.price)),
                                        'quantity': 1,
                                        'total': round(float(product.price)),
                                        'slug': product.slug})
    return JsonResponse({'cart_total': round(request.session['cart_size'], 2)})


def remove_from_cart_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    product_slug = request.GET.get('product_slug')
    print(request.session['cart'], product_slug)
    for p, product in enumerate(request.session['cart']):
        if product['cart_id'] == product_slug:
            del request.session['cart'][p]
    request.session['cart_cost'] = 0
    for product in request.session['cart']:
        request.session['cart_cost'] += product['total']
    request.session['cart_size'] = len(request.session['cart'])

    return JsonResponse({'cart_total': len(request.session['cart']),
                         'cart_total_cost': request.session['cart_cost']})



# def change_item_quantity_view(request):
#     if not request.session.session_key:
#         request.session.create()
#         request.session['cart'] = []
#         request.session['cart_cost'] = 0
#         request.session['cart_size'] = 0
#         cart = request.session['cart']
#         cart_size = request.session['cart_size']
#     else:
#         cart = request.session['cart']
#         cart_size = request.session['cart_size']
#     quantity = request.GET.get('quantity')
#     product_id = request.GET.get('item_id')
#     print(quantity, product_id)
#     item_total = 0
#     for line, product in enumerate(request.session['cart']):
#         if int(product['id']) == int(product_id):
#             price = request.session['cart'][line]['price']
#             request.session['cart'][line]['quantity'] = quantity
#             request.session['cart'][line]['total'] = float(price) * int(quantity)
#             item_total = request.session['cart'][line]['total']
#     request.session['cart_cost'] = 0
#     for product in request.session['cart']:
#         request.session['cart_cost'] += product['total']
#     return JsonResponse({'item_total': item_total,
#                          'cart_total_cost': request.session['cart_cost']})


def checkout_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    cart_cost = request.session['cart_cost']
    context = {
        'cart': cart,
        'cart_size': cart_size,
        'cart_cost': cart_cost,
    }
    return render(request, 'check_out.html', context)


def order_create_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    cart_cost = request.session['cart_cost']
    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart,
        'cart_size': cart_size,
        'cart_cost': cart_cost,
    }
    return render(request, 'order.html', context)


def make_order_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    form = OrderForm(request.POST or None)
    if form.is_valid():
        card = form.cleaned_data['card']
        cvv = form.cleaned_data['cvv']
        total = request.session['cart_cost']
        date = form.cleaned_data['date']
        new_order = Order.objects.create(
            user=request.user,
            card=card,
            date=date,
            cvv=cvv,
            total=total
        )
        new_order.save()
        for product in request.session['cart']:
            # obj = Foo.objects.latest('id')
            new_key = Key.objects.create(
                key=randint(1000000000, 9999999999)
            )
            new_key.save()
            new_cart = Cart.objects.create(
                product=Game.objects.get(id=product['id']),
                item_cost=product['price'],
                key=new_key,
            )
            new_cart.save()
            new_order.carts.add(new_cart)
        context_id = new_order.id
        context = {
            'order_id': context_id,
            'cart': cart,
            'cart_size': cart_size,

        }
        request.session['cart'] = []
        request.session['cart_size'] = 0
        request.session['cart_cost'] = 0
        return render(request, 'thank_you.html', context)

def user_orders_view(request):
    if not request.session.session_key:
        request.session.create()
        request.session['cart'] = []
        request.session['cart_cost'] = 0
        request.session['cart_size'] = 0
        request.session['cart_id'] = 0
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    else:
        cart = request.session['cart']
        cart_size = request.session['cart_size']
    orders = Order.objects.filter(user=request.user).order_by('-id')
    carts = Cart.objects.all()
    products = Game.objects.all()
    account = []
    for order_id, order in enumerate(orders):
        account.append({'order_id': order.id,
                        'order_total': order.total,
                        'order_date': order.date,
                        'carts': []})
        for cart in carts:
            # if cart.order.id == order.id:
                account[order_id]['carts'].append({'cart_cost': cart.item_cost,
                                                   'product_name': cart.product.title
                                                   })
    context = {
        'account': account,
        'cart_size': cart_size
    }
    return render(request, 'account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = RegistrationForm(request.POST or None)
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def account_view(request):
    form = RegistrationForm(request.POST or None)
    user_id = request.se
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)



